import sys
import os
import numpy as np
import qdarktheme
import cv2
import json
from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QHBoxLayout,
    QFileDialog,
    QGraphicsItem,
    QGraphicsEllipseItem,
    QGraphicsLineItem,
    QTableWidgetItem,
    QGraphicsPolygonItem,
    QTableWidgetSelectionRange,
    QSpacerItem,
    QHeaderView,
)
from PyQt6.QtGui import (
    QPixmap,
    QColor,
    QPen,
    QBrush,
    QPolygonF,
    QIcon,
    QCursor,
    QKeySequence,
    QShortcut,
)
from PyQt6.QtCore import Qt, QPointF, QTimer, QModelIndex

from .photo_viewer import PhotoViewer
from .sam_model import SamModel
from .utils import mask_to_pixmap
from .controls import ControlPanel, RightPanel
from .custom_file_system_model import CustomFileSystemModel
from .editable_vertex import EditableVertexItem
from .hoverable_polygon_item import HoverablePolygonItem
from .hoverable_pixelmap_item import HoverablePixmapItem
from .numeric_table_widget_item import NumericTableWidgetItem


class MainWindow(QMainWindow):
    def __init__(self, sam_model):
        super().__init__()
        self.setWindowTitle("LazyLabel by DNC")

        icon_path = os.path.join(
            os.path.dirname(__file__), "demo_pictures", "logo2.png"
        )
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))

        self.setGeometry(50, 50, 1600, 900)

        self.sam_model = sam_model
        self.mode = "sam_points"
        self.previous_mode = "sam_points"
        self.current_image_path = None
        self.current_file_index = QModelIndex()

        self.next_class_id = 0
        self.class_aliases = {}

        self._original_point_radius = 0.3
        self._original_line_thickness = 0.5
        self.point_radius = self._original_point_radius
        self.line_thickness = self._original_line_thickness

        self.pan_multiplier = 1.0
        self.polygon_join_threshold = 2

        self.point_items, self.positive_points, self.negative_points = [], [], []
        self.polygon_points, self.polygon_preview_items = [], []
        self.rubber_band_line = None

        self.segments, self.segment_items, self.highlight_items = [], {}, []
        self.is_dragging_polygon, self.drag_start_pos, self.drag_initial_vertices = (
            False,
            None,
            {},
        )

        self.control_panel = ControlPanel()
        self.right_panel = RightPanel()
        self.viewer = PhotoViewer(self)
        self.viewer.setMouseTracking(True)
        self.file_model = CustomFileSystemModel()
        self.right_panel.file_tree.setModel(self.file_model)
        self.right_panel.file_tree.setColumnWidth(0, 200)
        file_tree = self.right_panel.file_tree
        header = file_tree.header()
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)

        main_layout = QHBoxLayout()
        main_layout.addWidget(self.control_panel)
        main_layout.addWidget(self.viewer, 1)
        main_layout.addWidget(self.right_panel)
        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

        self.control_panel.device_label.setText(
            f"Device: {str(self.sam_model.device).upper()}"
        )
        self.setup_connections()
        self.set_sam_mode()
        self.set_annotation_size(10)

    def setup_connections(self):
        self._original_mouse_press = self.viewer.scene().mousePressEvent
        self._original_mouse_move = self.viewer.scene().mouseMoveEvent
        self._original_mouse_release = self.viewer.scene().mouseReleaseEvent

        self.viewer.scene().mousePressEvent = self.scene_mouse_press
        self.viewer.scene().mouseMoveEvent = self.scene_mouse_move
        self.viewer.scene().mouseReleaseEvent = self.scene_mouse_release

        self.right_panel.btn_open_folder.clicked.connect(self.open_folder_dialog)
        self.right_panel.file_tree.doubleClicked.connect(self.load_selected_image)
        self.right_panel.btn_merge_selection.clicked.connect(
            self.assign_selected_to_class
        )
        self.right_panel.btn_delete_selection.clicked.connect(
            self.delete_selected_segments
        )
        self.right_panel.segment_table.itemSelectionChanged.connect(
            self.highlight_selected_segments
        )
        self.right_panel.class_table.itemChanged.connect(self.handle_alias_change)
        self.right_panel.btn_reassign_classes.clicked.connect(self.reassign_class_ids)
        self.right_panel.class_filter_combo.currentIndexChanged.connect(
            self.update_segment_table
        )

        self.control_panel.btn_sam_mode.clicked.connect(self.set_sam_mode)
        self.control_panel.btn_polygon_mode.clicked.connect(self.set_polygon_mode)
        self.control_panel.btn_selection_mode.clicked.connect(
            self.toggle_selection_mode
        )
        self.control_panel.btn_clear_points.clicked.connect(self.clear_all_points)
        self.control_panel.btn_fit_view.clicked.connect(self.viewer.fitInView)

        self.control_panel.size_slider.valueChanged.connect(self.set_annotation_size)
        self.control_panel.pan_slider.valueChanged.connect(self.set_pan_multiplier)
        self.control_panel.join_slider.valueChanged.connect(
            self.set_polygon_join_threshold
        )

        self.control_panel.chk_save_npz.stateChanged.connect(
            self.handle_save_checkbox_change
        )
        self.control_panel.chk_save_txt.stateChanged.connect(
            self.handle_save_checkbox_change
        )

        self.control_panel.btn_toggle_visibility.clicked.connect(self.toggle_left_panel)
        self.right_panel.btn_toggle_visibility.clicked.connect(self.toggle_right_panel)

        QShortcut(QKeySequence(Qt.Key.Key_Right), self, self.load_next_image)
        QShortcut(QKeySequence(Qt.Key.Key_Left), self, self.load_previous_image)
        QShortcut(QKeySequence(Qt.Key.Key_1), self, self.set_sam_mode)
        QShortcut(QKeySequence(Qt.Key.Key_2), self, self.set_polygon_mode)
        QShortcut(QKeySequence(Qt.Key.Key_E), self, self.toggle_selection_mode)
        QShortcut(QKeySequence(Qt.Key.Key_Q), self, self.toggle_pan_mode)
        QShortcut(QKeySequence(Qt.Key.Key_R), self, self.toggle_edit_mode)
        QShortcut(QKeySequence(Qt.Key.Key_C), self, self.clear_all_points)
        QShortcut(QKeySequence(Qt.Key.Key_Escape), self, self.handle_escape_press)
        QShortcut(QKeySequence(Qt.Key.Key_V), self, self.delete_selected_segments)
        QShortcut(
            QKeySequence(Qt.Key.Key_Backspace), self, self.delete_selected_segments
        )
        QShortcut(QKeySequence(Qt.Key.Key_M), self, self.handle_merge_press)
        QShortcut(QKeySequence("Ctrl+Z"), self, self.undo_last_action)
        QShortcut(
            QKeySequence("Ctrl+A"), self, self.right_panel.segment_table.selectAll
        )
        QShortcut(QKeySequence(Qt.Key.Key_Space), self, self.handle_space_press)
        QShortcut(QKeySequence(Qt.Key.Key_Return), self, self.handle_enter_press)
        QShortcut(QKeySequence(Qt.Key.Key_Enter), self, self.handle_enter_press)
        QShortcut(QKeySequence(Qt.Key.Key_Period), self, self.viewer.fitInView)

    def toggle_left_panel(self):
        is_visible = self.control_panel.main_controls_widget.isVisible()
        self.control_panel.main_controls_widget.setVisible(not is_visible)
        if is_visible:
            self.control_panel.btn_toggle_visibility.setText("> Show")
            self.control_panel.setFixedWidth(
                self.control_panel.btn_toggle_visibility.sizeHint().width() + 20
            )
        else:
            self.control_panel.btn_toggle_visibility.setText("< Hide")
            self.control_panel.setFixedWidth(250)

    def toggle_right_panel(self):
        is_visible = self.right_panel.main_controls_widget.isVisible()
        self.right_panel.main_controls_widget.setVisible(not is_visible)
        layout = self.right_panel.v_layout

        if is_visible:  # Content is now hidden
            layout.addStretch(1)
            self.right_panel.btn_toggle_visibility.setText("< Show")
            self.right_panel.setFixedWidth(
                self.right_panel.btn_toggle_visibility.sizeHint().width() + 20
            )
        else:  # Content is now visible
            # Remove the stretch so the content can expand
            for i in range(layout.count()):
                item = layout.itemAt(i)
                if isinstance(item, QSpacerItem):
                    layout.removeItem(item)
                    break
            self.right_panel.btn_toggle_visibility.setText("Hide >")
            self.right_panel.setFixedWidth(350)

    def handle_save_checkbox_change(self):
        is_npz_checked = self.control_panel.chk_save_npz.isChecked()
        is_txt_checked = self.control_panel.chk_save_txt.isChecked()

        if not is_npz_checked and not is_txt_checked:
            sender = self.sender()
            if sender == self.control_panel.chk_save_npz:
                self.control_panel.chk_save_txt.setChecked(True)
            else:
                self.control_panel.chk_save_npz.setChecked(True)

    def set_annotation_size(self, value):
        multiplier = value / 10.0
        self.point_radius = self._original_point_radius * multiplier
        self.line_thickness = self._original_line_thickness * multiplier

        self.control_panel.size_label.setText(f"Annotation Size: {multiplier:.1f}x")

        if self.control_panel.size_slider.value() != value:
            self.control_panel.size_slider.setValue(value)

        self.display_all_segments()
        self.clear_all_points()

    def set_pan_multiplier(self, value):
        self.pan_multiplier = value / 10.0
        self.control_panel.pan_label.setText(f"Pan Speed: {self.pan_multiplier:.1f}x")

    def set_polygon_join_threshold(self, value):
        self.polygon_join_threshold = value
        self.control_panel.join_label.setText(f"Polygon Join Distance: {value}px")

    def handle_escape_press(self):
        self.right_panel.segment_table.clearSelection()
        self.right_panel.class_table.clearSelection()
        self.clear_all_points()
        self.viewer.setFocus()

    def handle_space_press(self):
        if self.mode == "polygon" and self.polygon_points:
            self.finalize_polygon()
        else:
            self.save_current_segment()

    def handle_enter_press(self):
        if self.mode == "polygon" and self.polygon_points:
            self.finalize_polygon()
        else:
            self.save_output_to_npz()

    def handle_merge_press(self):
        self.assign_selected_to_class()
        self.right_panel.segment_table.clearSelection()

    def show_notification(self, message, duration=3000):
        self.control_panel.notification_label.setText(message)
        QTimer.singleShot(
            duration, lambda: self.control_panel.notification_label.clear()
        )

    def _get_color_for_class(self, class_id):
        if class_id is None:
            return QColor.fromHsv(0, 0, 128)
        hue = int((class_id * 222.4922359) % 360)
        color = QColor.fromHsv(hue, 220, 220)
        if not color.isValid():
            return QColor(Qt.GlobalColor.white)
        return color

    def set_mode(self, mode_name, is_toggle=False):
        if self.mode == "selection" and mode_name not in ["selection", "edit"]:
            self.right_panel.segment_table.clearSelection()
        if self.mode == "edit" and mode_name != "edit":
            self.display_all_segments()

        if not is_toggle and self.mode not in ["selection", "edit"]:
            self.previous_mode = self.mode

        self.mode = mode_name
        self.control_panel.mode_label.setText(
            f"Mode: {mode_name.replace('_', ' ').title()}"
        )
        self.clear_all_points()

        cursor_map = {
            "sam_points": Qt.CursorShape.CrossCursor,
            "polygon": Qt.CursorShape.CrossCursor,
            "selection": Qt.CursorShape.ArrowCursor,
            "edit": Qt.CursorShape.SizeAllCursor,
            "pan": Qt.CursorShape.OpenHandCursor,
        }
        self.viewer.set_cursor(cursor_map.get(self.mode, Qt.CursorShape.ArrowCursor))

        self.viewer.setDragMode(
            self.viewer.DragMode.ScrollHandDrag
            if self.mode == "pan"
            else self.viewer.DragMode.NoDrag
        )

    def set_sam_mode(self):
        self.set_mode("sam_points")

    def set_polygon_mode(self):
        self.set_mode("polygon")

    def toggle_mode(self, new_mode):
        if self.mode == new_mode:
            self.set_mode(self.previous_mode, is_toggle=True)
        else:
            if self.mode not in ["selection", "edit"]:
                self.previous_mode = self.mode
            self.set_mode(new_mode, is_toggle=True)

    def toggle_pan_mode(self):
        self.toggle_mode("pan")

    def toggle_selection_mode(self):
        self.toggle_mode("selection")

    def toggle_edit_mode(self):
        selected_indices = self.get_selected_segment_indices()

        if self.mode == "edit":
            self.set_mode("selection", is_toggle=True)
            return

        if not selected_indices:
            self.show_notification("Select a polygon to edit.")
            return

        can_edit = any(
            self.segments[i].get("type") == "Polygon" for i in selected_indices
        )

        if not can_edit:
            self.show_notification("Only polygon segments can be edited.")
            return

        self.set_mode("edit", is_toggle=True)
        self.display_all_segments()

    def open_folder_dialog(self):
        folder_path = QFileDialog.getExistingDirectory(self, "Select Image Folder")
        if folder_path:
            self.right_panel.file_tree.setRootIndex(
                self.file_model.setRootPath(folder_path)
            )
        self.viewer.setFocus()

    def load_selected_image(self, index):
        if not index.isValid() or not self.file_model.isDir(index.parent()):
            return

        self.current_file_index = index
        path = self.file_model.filePath(index)

        if os.path.isfile(path) and path.lower().endswith(
            (".png", ".jpg", ".jpeg", ".tiff", ".tif")
        ):
            self.current_image_path = path
            pixmap = QPixmap(self.current_image_path)
            if not pixmap.isNull():
                self.reset_state()
                self.viewer.set_photo(pixmap)
                self.sam_model.set_image(self.current_image_path)
                self.load_class_aliases()
                self.load_existing_mask()
                self.right_panel.file_tree.setCurrentIndex(index)
                self.viewer.setFocus()

    def load_next_image(self):
        if not self.current_file_index.isValid():
            return

        if self.control_panel.chk_auto_save.isChecked():
            self.save_output_to_npz()

        row = self.current_file_index.row()
        parent = self.current_file_index.parent()
        if row + 1 < self.file_model.rowCount(parent):
            next_index = self.file_model.index(row + 1, 0, parent)
            self.load_selected_image(next_index)

    def load_previous_image(self):
        if not self.current_file_index.isValid():
            return

        if self.control_panel.chk_auto_save.isChecked():
            self.save_output_to_npz()

        row = self.current_file_index.row()
        parent = self.current_file_index.parent()
        if row > 0:
            prev_index = self.file_model.index(row - 1, 0, parent)
            self.load_selected_image(prev_index)

    def reset_state(self):
        self.clear_all_points()
        self.segments.clear()
        self.class_aliases.clear()
        self.next_class_id = 0
        self.update_all_lists()
        items_to_remove = [
            item
            for item in self.viewer.scene().items()
            if item is not self.viewer._pixmap_item
        ]
        for item in items_to_remove:
            self.viewer.scene().removeItem(item)
        self.segment_items.clear()
        self.highlight_items.clear()

    def keyPressEvent(self, event):
        key, mods = event.key(), event.modifiers()

        if event.isAutoRepeat() and key not in {
            Qt.Key.Key_W,
            Qt.Key.Key_A,
            Qt.Key.Key_S,
            Qt.Key.Key_D,
        }:
            return

        shift_multiplier = 5.0 if mods & Qt.KeyboardModifier.ShiftModifier else 1.0

        if key == Qt.Key.Key_W:
            amount = int(
                self.viewer.height() * 0.1 * self.pan_multiplier * shift_multiplier
            )
            self.viewer.verticalScrollBar().setValue(
                self.viewer.verticalScrollBar().value() - amount
            )
        elif key == Qt.Key.Key_S:
            amount = int(
                self.viewer.height() * 0.1 * self.pan_multiplier * shift_multiplier
            )
            self.viewer.verticalScrollBar().setValue(
                self.viewer.verticalScrollBar().value() + amount
            )
        elif key == Qt.Key.Key_A:
            amount = int(
                self.viewer.width() * 0.1 * self.pan_multiplier * shift_multiplier
            )
            self.viewer.horizontalScrollBar().setValue(
                self.viewer.horizontalScrollBar().value() - amount
            )
        elif key == Qt.Key.Key_D:
            amount = int(
                self.viewer.width() * 0.1 * self.pan_multiplier * shift_multiplier
            )
            self.viewer.horizontalScrollBar().setValue(
                self.viewer.horizontalScrollBar().value() + amount
            )
        elif (
            key == Qt.Key.Key_Equal or key == Qt.Key.Key_Plus
        ) and mods == Qt.KeyboardModifier.ControlModifier:
            current_val = self.control_panel.size_slider.value()
            self.control_panel.size_slider.setValue(current_val + 1)
        elif key == Qt.Key.Key_Minus and mods == Qt.KeyboardModifier.ControlModifier:
            current_val = self.control_panel.size_slider.value()
            self.control_panel.size_slider.setValue(current_val - 1)
        else:
            super().keyPressEvent(event)

    def scene_mouse_press(self, event):
        self._original_mouse_press(event)
        if event.isAccepted():
            return

        if self.mode == "pan":
            self.viewer.set_cursor(Qt.CursorShape.ClosedHandCursor)

        pos = event.scenePos()
        if (
            self.viewer._pixmap_item.pixmap().isNull()
            or not self.viewer._pixmap_item.pixmap().rect().contains(pos.toPoint())
        ):
            return
        if self.mode == "sam_points":
            if event.button() == Qt.MouseButton.LeftButton:
                self.add_point(pos, positive=True)
                self.update_segmentation()
            elif event.button() == Qt.MouseButton.RightButton:
                self.add_point(pos, positive=False)
                self.update_segmentation()
        elif self.mode == "polygon":
            if event.button() == Qt.MouseButton.LeftButton:
                self.handle_polygon_click(pos)
        elif self.mode == "selection":
            if event.button() == Qt.MouseButton.LeftButton:
                self.handle_segment_selection_click(pos)
        elif self.mode == "edit":
            self.drag_start_pos = pos
            self.is_dragging_polygon = True
            selected_indices = self.get_selected_segment_indices()
            self.drag_initial_vertices = {
                i: list(self.segments[i]["vertices"])
                for i in selected_indices
                if self.segments[i].get("type") == "Polygon"
            }

    def scene_mouse_move(self, event):
        pos = event.scenePos()
        if self.mode == "edit" and self.is_dragging_polygon:
            delta = pos - self.drag_start_pos
            for i, initial_verts in self.drag_initial_vertices.items():
                self.segments[i]["vertices"] = [
                    QPointF(v.x() + delta.x(), v.y() + delta.y()) for v in initial_verts
                ]
                self.update_polygon_visuals(i)
        elif self.mode == "polygon" and self.polygon_points:
            if self.rubber_band_line is None:
                self.rubber_band_line = QGraphicsLineItem()
                line_color = QColor(Qt.GlobalColor.white)
                line_color.setAlpha(150)
                self.rubber_band_line.setPen(
                    QPen(line_color, self.line_thickness, Qt.PenStyle.DotLine)
                )
                self.viewer.scene().addItem(self.rubber_band_line)
            self.rubber_band_line.setLine(
                self.polygon_points[-1].x(),
                self.polygon_points[-1].y(),
                pos.x(),
                pos.y(),
            )
            self.rubber_band_line.show()
        else:
            self._original_mouse_move(event)

    def scene_mouse_release(self, event):
        if self.mode == "pan":
            self.viewer.set_cursor(Qt.CursorShape.OpenHandCursor)
        if self.mode == "edit" and self.is_dragging_polygon:
            self.is_dragging_polygon = False
            self.drag_initial_vertices.clear()
        self._original_mouse_release(event)

    def undo_last_action(self):
        if self.mode == "polygon" and self.polygon_points:
            self.polygon_points.pop()
            for item in self.polygon_preview_items:
                if item.scene():
                    self.viewer.scene().removeItem(item)
            self.polygon_preview_items.clear()
            for point in self.polygon_points:
                point_diameter = self.point_radius * 2
                point_color = QColor(Qt.GlobalColor.blue)
                point_color.setAlpha(150)
                dot = QGraphicsEllipseItem(
                    point.x() - self.point_radius,
                    point.y() - self.point_radius,
                    point_diameter,
                    point_diameter,
                )
                dot.setBrush(QBrush(point_color))
                dot.setPen(QPen(Qt.GlobalColor.transparent))
                self.viewer.scene().addItem(dot)
                self.polygon_preview_items.append(dot)
            self.draw_polygon_preview()
        elif self.mode == "sam_points" and self.point_items:
            item_to_remove = self.point_items.pop()
            point_pos = item_to_remove.rect().topLeft() + QPointF(
                self.point_radius, self.point_radius
            )
            point_coords = [int(point_pos.x()), int(point_pos.y())]
            if point_coords in self.positive_points:
                self.positive_points.remove(point_coords)
            elif point_coords in self.negative_points:
                self.negative_points.remove(point_coords)
            self.viewer.scene().removeItem(item_to_remove)
            self.update_segmentation()

    def _update_next_class_id(self):
        all_ids = {
            seg.get("class_id")
            for seg in self.segments
            if seg.get("class_id") is not None
        }
        if not all_ids:
            self.next_class_id = 0
        else:
            self.next_class_id = max(all_ids) + 1

    def finalize_polygon(self):
        if len(self.polygon_points) < 3:
            return
        if self.rubber_band_line:
            self.viewer.scene().removeItem(self.rubber_band_line)
            self.rubber_band_line = None
        self.segments.append(
            {
                "vertices": list(self.polygon_points),
                "type": "Polygon",
                "mask": None,
                "class_id": self.next_class_id,
            }
        )
        self._update_next_class_id()
        self.polygon_points.clear()
        for item in self.polygon_preview_items:
            self.viewer.scene().removeItem(item)
        self.polygon_preview_items.clear()
        self.update_all_lists()

    def handle_segment_selection_click(self, pos):
        x, y = int(pos.x()), int(pos.y())
        for i in range(len(self.segments) - 1, -1, -1):
            seg = self.segments[i]
            mask = (
                self.rasterize_polygon(seg["vertices"])
                if seg["type"] == "Polygon"
                else seg.get("mask")
            )
            if (
                mask is not None
                and y < mask.shape[0]
                and x < mask.shape[1]
                and mask[y, x]
            ):
                for j in range(self.right_panel.segment_table.rowCount()):
                    item = self.right_panel.segment_table.item(j, 0)
                    if item and item.data(Qt.ItemDataRole.UserRole) == i:
                        table = self.right_panel.segment_table
                        is_selected = table.item(j, 0).isSelected()
                        range_to_select = QTableWidgetSelectionRange(
                            j, 0, j, table.columnCount() - 1
                        )
                        table.setRangeSelected(range_to_select, not is_selected)
                        return
        self.viewer.setFocus()

    def assign_selected_to_class(self):
        selected_indices = self.get_selected_segment_indices()
        if not selected_indices:
            return

        existing_class_ids = [
            self.segments[i]["class_id"]
            for i in selected_indices
            if self.segments[i].get("class_id") is not None
        ]

        if existing_class_ids:
            target_class_id = min(existing_class_ids)
        else:
            target_class_id = self.next_class_id

        for i in selected_indices:
            self.segments[i]["class_id"] = target_class_id

        self._update_next_class_id()
        self.update_all_lists()
        self.viewer.setFocus()

    def rasterize_polygon(self, vertices):
        if not vertices or self.viewer._pixmap_item.pixmap().isNull():
            return None
        h, w = (
            self.viewer._pixmap_item.pixmap().height(),
            self.viewer._pixmap_item.pixmap().width(),
        )
        points_np = np.array([[p.x(), p.y()] for p in vertices], dtype=np.int32)
        mask = np.zeros((h, w), dtype=np.uint8)
        cv2.fillPoly(mask, [points_np], 1)
        return mask.astype(bool)

    def display_all_segments(self):
        for i, items in self.segment_items.items():
            for item in items:
                self.viewer.scene().removeItem(item)
        self.segment_items.clear()
        selected_indices = self.get_selected_segment_indices()

        for i, seg_dict in enumerate(self.segments):
            self.segment_items[i] = []
            class_id = seg_dict.get("class_id")
            base_color = self._get_color_for_class(class_id)

            if seg_dict["type"] == "Polygon":
                poly_item = HoverablePolygonItem(QPolygonF(seg_dict["vertices"]))
                default_brush = QBrush(
                    QColor(base_color.red(), base_color.green(), base_color.blue(), 70)
                )
                hover_brush = QBrush(
                    QColor(base_color.red(), base_color.green(), base_color.blue(), 170)
                )
                poly_item.set_brushes(default_brush, hover_brush)
                poly_item.setPen(QPen(Qt.GlobalColor.transparent))
                self.viewer.scene().addItem(poly_item)
                self.segment_items[i].append(poly_item)
                base_color.setAlpha(150)
                vertex_color = QBrush(base_color)
                point_diameter = self.point_radius * 2
                for v in seg_dict["vertices"]:
                    dot = QGraphicsEllipseItem(
                        v.x() - self.point_radius,
                        v.y() - self.point_radius,
                        point_diameter,
                        point_diameter,
                    )
                    dot.setBrush(vertex_color)
                    dot.setPen(QPen(Qt.GlobalColor.transparent))
                    self.viewer.scene().addItem(dot)
                    self.segment_items[i].append(dot)
                if self.mode == "edit" and i in selected_indices:
                    handle_diameter = self.point_radius * 2
                    for idx, v in enumerate(seg_dict["vertices"]):
                        vertex_item = EditableVertexItem(
                            self,
                            i,
                            idx,
                            -handle_diameter / 2,
                            -handle_diameter / 2,
                            handle_diameter,
                            handle_diameter,
                        )
                        vertex_item.setPos(v)
                        self.viewer.scene().addItem(vertex_item)
                        self.segment_items[i].append(vertex_item)
            elif seg_dict.get("mask") is not None:
                default_pixmap = mask_to_pixmap(
                    seg_dict["mask"], base_color.getRgb()[:3], alpha=70
                )
                hover_pixmap = mask_to_pixmap(
                    seg_dict["mask"], base_color.getRgb()[:3], alpha=170
                )
                pixmap_item = HoverablePixmapItem()
                pixmap_item.set_pixmaps(default_pixmap, hover_pixmap)
                self.viewer.scene().addItem(pixmap_item)
                pixmap_item.setZValue(i + 1)
                self.segment_items[i].append(pixmap_item)
        self.highlight_selected_segments()

    def update_vertex_pos(self, seg_idx, vtx_idx, new_pos):
        self.segments[seg_idx]["vertices"][vtx_idx] = new_pos
        self.update_polygon_visuals(seg_idx)

    def update_polygon_visuals(self, segment_index):
        items = self.segment_items.get(segment_index, [])
        for item in items:
            if isinstance(item, HoverablePolygonItem):
                item.setPolygon(QPolygonF(self.segments[segment_index]["vertices"]))
                break

    def highlight_selected_segments(self):
        if hasattr(self, "highlight_items"):
            for item in self.highlight_items:
                self.viewer.scene().removeItem(item)
        self.highlight_items.clear()
        selected_indices = self.get_selected_segment_indices()
        for i in selected_indices:
            seg = self.segments[i]
            mask = (
                self.rasterize_polygon(seg["vertices"])
                if seg["type"] == "Polygon"
                else seg.get("mask")
            )
            if mask is not None:
                pixmap = mask_to_pixmap(mask, (255, 255, 255))
                highlight_item = self.viewer.scene().addPixmap(pixmap)
                highlight_item.setZValue(100)
                self.highlight_items.append(highlight_item)

    def update_all_lists(self):
        self.update_class_list()
        self.update_class_filter_combo()
        self.update_segment_table()
        self.display_all_segments()

    def update_segment_table(self):
        table = self.right_panel.segment_table
        table.blockSignals(True)
        selected_indices = self.get_selected_segment_indices()
        table.clearContents()
        table.setRowCount(0)
        filter_text = self.right_panel.class_filter_combo.currentText()
        show_all = filter_text == "All Classes"
        filter_class_id = -1
        if not show_all:
            try:
                filter_class_id = int(filter_text.split("(ID: ")[1][:-1])
            except (ValueError, IndexError):
                pass

        display_segments = []
        for i, seg in enumerate(self.segments):
            if show_all or seg.get("class_id") == filter_class_id:
                display_segments.append((i, seg))

        table.setRowCount(len(display_segments))

        for row, (original_index, seg) in enumerate(display_segments):
            class_id = seg.get("class_id")
            color = self._get_color_for_class(class_id)
            class_id_str = str(class_id) if class_id is not None else "N/A"

            alias_str = "N/A"
            if class_id is not None:
                alias_str = self.class_aliases.get(class_id, str(class_id))
            alias_item = QTableWidgetItem(alias_str)

            index_item = NumericTableWidgetItem(str(original_index + 1))
            class_item = NumericTableWidgetItem(class_id_str)

            index_item.setFlags(index_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
            class_item.setFlags(class_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
            alias_item.setFlags(alias_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
            index_item.setData(Qt.ItemDataRole.UserRole, original_index)

            table.setItem(row, 0, index_item)
            table.setItem(row, 1, class_item)
            table.setItem(row, 2, alias_item)

            for col in range(table.columnCount()):
                if table.item(row, col):
                    table.item(row, col).setBackground(QBrush(color))

        table.setSortingEnabled(False)
        for row in range(table.rowCount()):
            item = table.item(row, 0)
            if item and item.data(Qt.ItemDataRole.UserRole) in selected_indices:
                table.selectRow(row)
        table.setSortingEnabled(True)

        table.blockSignals(False)
        self.viewer.setFocus()

    def update_class_list(self):
        class_table = self.right_panel.class_table
        class_table.blockSignals(True)

        preserved_aliases = self.class_aliases.copy()
        unique_class_ids = sorted(
            list(
                {
                    seg.get("class_id")
                    for seg in self.segments
                    if seg.get("class_id") is not None
                }
            )
        )

        new_aliases = {}
        for cid in unique_class_ids:
            new_aliases[cid] = preserved_aliases.get(cid, str(cid))

        self.class_aliases = new_aliases

        class_table.clearContents()
        class_table.setRowCount(len(unique_class_ids))
        for row, cid in enumerate(unique_class_ids):
            alias_item = QTableWidgetItem(self.class_aliases.get(cid))
            id_item = QTableWidgetItem(str(cid))
            id_item.setFlags(id_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
            color = self._get_color_for_class(cid)
            alias_item.setBackground(QBrush(color))
            id_item.setBackground(QBrush(color))
            class_table.setItem(row, 0, alias_item)
            class_table.setItem(row, 1, id_item)

        class_table.blockSignals(False)

    def update_class_filter_combo(self):
        combo = self.right_panel.class_filter_combo
        unique_class_ids = sorted(
            list(
                {
                    seg.get("class_id")
                    for seg in self.segments
                    if seg.get("class_id") is not None
                }
            )
        )
        current_selection = combo.currentText()
        combo.blockSignals(True)
        combo.clear()
        combo.addItem("All Classes")
        combo.addItems(
            [
                f"{self.class_aliases.get(cid, cid)} (ID: {cid})"
                for cid in unique_class_ids
            ]
        )
        if combo.findText(current_selection) > -1:
            combo.setCurrentText(current_selection)
        else:
            combo.setCurrentIndex(0)
        combo.blockSignals(False)

    def reassign_class_ids(self):
        class_table = self.right_panel.class_table
        ordered_ids = []
        for row in range(class_table.rowCount()):
            id_item = class_table.item(row, 1)
            if id_item and id_item.text():
                try:
                    ordered_ids.append(int(id_item.text()))
                except ValueError:
                    continue
        id_map = {old_id: new_id for new_id, old_id in enumerate(ordered_ids)}
        for seg in self.segments:
            old_id = seg.get("class_id")
            if old_id in id_map:
                seg["class_id"] = id_map[old_id]
        new_aliases = {
            id_map[old_id]: self.class_aliases.get(old_id, str(old_id))
            for old_id in ordered_ids
            if old_id in self.class_aliases
        }
        self.class_aliases = new_aliases
        self._update_next_class_id()
        self.update_all_lists()
        self.viewer.setFocus()

    def handle_alias_change(self, item):
        if item.column() != 0:
            return
        class_table = self.right_panel.class_table
        class_table.blockSignals(True)
        id_item = class_table.item(item.row(), 1)
        if id_item:
            try:
                class_id = int(id_item.text())
                self.class_aliases[class_id] = item.text()
            except (ValueError, AttributeError):
                pass
        class_table.blockSignals(False)

        self.update_class_filter_combo()
        self.update_segment_table()

    def get_selected_segment_indices(self):
        table = self.right_panel.segment_table
        selected_items = table.selectedItems()
        selected_rows = sorted(list({item.row() for item in selected_items}))
        return [
            table.item(row, 0).data(Qt.ItemDataRole.UserRole)
            for row in selected_rows
            if table.item(row, 0)
        ]

    def save_output_to_npz(self):
        save_npz = self.control_panel.chk_save_npz.isChecked()
        save_txt = self.control_panel.chk_save_txt.isChecked()
        save_aliases = self.control_panel.chk_save_class_aliases.isChecked()

        if not self.current_image_path or not any([save_npz, save_txt, save_aliases]):
            return

        self.right_panel.status_label.setText("Saving...")
        QApplication.processEvents()

        saved_something = False

        if save_npz or save_txt:
            if not self.segments:
                self.show_notification("No segments to save.")
            else:
                h, w = (
                    self.viewer._pixmap_item.pixmap().height(),
                    self.viewer._pixmap_item.pixmap().width(),
                )
                class_table = self.right_panel.class_table
                ordered_ids = [
                    int(class_table.item(row, 1).text())
                    for row in range(class_table.rowCount())
                    if class_table.item(row, 1) is not None
                ]

                if not ordered_ids:
                    self.show_notification("No classes defined for mask saving.")
                else:
                    id_map = {
                        old_id: new_id for new_id, old_id in enumerate(ordered_ids)
                    }
                    num_final_classes = len(ordered_ids)
                    final_mask_tensor = np.zeros(
                        (h, w, num_final_classes), dtype=np.uint8
                    )

                    for seg in self.segments:
                        class_id = seg.get("class_id")
                        if class_id not in id_map:
                            continue
                        new_channel_idx = id_map[class_id]
                        mask = (
                            self.rasterize_polygon(seg["vertices"])
                            if seg["type"] == "Polygon"
                            else seg.get("mask")
                        )
                        if mask is not None:
                            final_mask_tensor[:, :, new_channel_idx] = np.logical_or(
                                final_mask_tensor[:, :, new_channel_idx], mask
                            )
                    if save_npz:
                        npz_path = os.path.splitext(self.current_image_path)[0] + ".npz"
                        np.savez_compressed(
                            npz_path, mask=final_mask_tensor.astype(np.uint8)
                        )
                        self.file_model.update_cache_for_path(npz_path)

                        self.file_model.set_highlighted_path(npz_path)
                        QTimer.singleShot(
                            1500, lambda: self.file_model.set_highlighted_path(None)
                        )
                        saved_something = True
                    if save_txt:
                        if self.control_panel.chk_yolo_use_alias.isChecked():
                            class_labels = [
                                class_table.item(row, 0).text()
                                for row in range(class_table.rowCount())
                            ]
                        else:
                            class_labels = list(range(num_final_classes))

                        txt_path = self.generate_yolo_annotations(
                            final_mask_tensor, class_labels
                        )
                        if txt_path:
                            self.file_model.update_cache_for_path(txt_path)
                        saved_something = True

        if save_aliases:
            aliases_path = os.path.splitext(self.current_image_path)[0] + ".json"
            aliases_to_save = {str(k): v for k, v in self.class_aliases.items()}
            with open(aliases_path, "w") as f:
                json.dump(aliases_to_save, f, indent=4)
            saved_something = True

        if saved_something:
            self.right_panel.status_label.setText("Saved!")
        else:
            self.right_panel.status_label.clear()

        QTimer.singleShot(3000, lambda: self.right_panel.status_label.clear())

    def generate_yolo_annotations(self, mask_tensor, class_labels):
        output_path = os.path.splitext(self.current_image_path)[0] + ".txt"
        h, w, num_channels = mask_tensor.shape

        directory_path = os.path.dirname(output_path)
        os.makedirs(directory_path, exist_ok=True)

        yolo_annotations = []
        for channel in range(num_channels):
            single_channel_image = mask_tensor[:, :, channel]
            if not np.any(single_channel_image):
                continue

            contours, _ = cv2.findContours(
                single_channel_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
            )

            class_label = class_labels[channel]
            for contour in contours:
                x, y, width, height = cv2.boundingRect(contour)
                center_x = (x + width / 2) / w
                center_y = (y + height / 2) / h
                normalized_width = width / w
                normalized_height = height / h
                yolo_entry = f"{class_label} {center_x} {center_y} {normalized_width} {normalized_height}"
                yolo_annotations.append(yolo_entry)

        if not yolo_annotations:
            return None

        with open(output_path, "w") as file:
            for annotation in yolo_annotations:
                file.write(annotation + "\n")

        return output_path

    def save_current_segment(self):
        if (
            self.mode != "sam_points"
            or not hasattr(self, "preview_mask_item")
            or not self.preview_mask_item
        ):
            return
        mask = self.sam_model.predict(self.positive_points, self.negative_points)
        if mask is not None:
            self.segments.append(
                {
                    "mask": mask,
                    "type": "SAM",
                    "vertices": None,
                    "class_id": self.next_class_id,
                }
            )
            self._update_next_class_id()
            self.clear_all_points()
            self.update_all_lists()

    def delete_selected_segments(self):
        selected_indices = self.get_selected_segment_indices()
        if not selected_indices:
            return
        for i in sorted(selected_indices, reverse=True):
            del self.segments[i]
        self._update_next_class_id()
        self.update_all_lists()
        self.viewer.setFocus()

    def load_class_aliases(self):
        if not self.current_image_path:
            return
        json_path = os.path.splitext(self.current_image_path)[0] + ".json"
        if os.path.exists(json_path):
            try:
                with open(json_path, "r") as f:
                    loaded_aliases = json.load(f)
                    # JSON loads keys as strings, convert them to int
                    self.class_aliases = {int(k): v for k, v in loaded_aliases.items()}
            except (json.JSONDecodeError, ValueError) as e:
                print(f"Error loading class aliases from {json_path}: {e}")
                self.class_aliases.clear()

    def load_existing_mask(self):
        if not self.current_image_path:
            return
        npz_path = os.path.splitext(self.current_image_path)[0] + ".npz"
        if os.path.exists(npz_path):
            with np.load(npz_path) as data:
                if "mask" in data:
                    mask_data = data["mask"]
                    if mask_data.ndim == 2:
                        mask_data = np.expand_dims(mask_data, axis=-1)
                    num_classes = mask_data.shape[2]
                    for i in range(num_classes):
                        class_mask = mask_data[:, :, i].astype(bool)
                        if np.any(class_mask):
                            self.segments.append(
                                {
                                    "mask": class_mask,
                                    "type": "Loaded",
                                    "vertices": None,
                                    "class_id": i,
                                }
                            )
                    self._update_next_class_id()
            self.update_all_lists()

    def add_point(self, pos, positive):
        point_list = self.positive_points if positive else self.negative_points
        point_list.append([int(pos.x()), int(pos.y())])
        point_color = (
            QColor(Qt.GlobalColor.green) if positive else QColor(Qt.GlobalColor.red)
        )
        point_color.setAlpha(150)
        point_diameter = self.point_radius * 2
        point_item = QGraphicsEllipseItem(
            pos.x() - self.point_radius,
            pos.y() - self.point_radius,
            point_diameter,
            point_diameter,
        )
        point_item.setBrush(QBrush(point_color))
        point_item.setPen(QPen(Qt.GlobalColor.transparent))
        self.viewer.scene().addItem(point_item)
        self.point_items.append(point_item)

    def update_segmentation(self):
        if hasattr(self, "preview_mask_item") and self.preview_mask_item:
            self.viewer.scene().removeItem(self.preview_mask_item)
        if not self.positive_points:
            return
        mask = self.sam_model.predict(self.positive_points, self.negative_points)
        if mask is not None:
            pixmap = mask_to_pixmap(mask, (255, 255, 0))
            self.preview_mask_item = self.viewer.scene().addPixmap(pixmap)
            self.preview_mask_item.setZValue(50)

    def clear_all_points(self):
        if self.rubber_band_line:
            self.viewer.scene().removeItem(self.rubber_band_line)
            self.rubber_band_line = None
        self.positive_points.clear()
        self.negative_points.clear()
        for item in self.point_items:
            self.viewer.scene().removeItem(item)
        self.point_items.clear()
        self.polygon_points.clear()
        for item in self.polygon_preview_items:
            self.viewer.scene().removeItem(item)
        self.polygon_preview_items.clear()
        if hasattr(self, "preview_mask_item") and self.preview_mask_item:
            self.viewer.scene().removeItem(self.preview_mask_item)
            self.preview_mask_item = None

    def handle_polygon_click(self, pos):
        if self.polygon_points and (
            (
                (pos.x() - self.polygon_points[0].x()) ** 2
                + (pos.y() - self.polygon_points[0].y()) ** 2
            )
            < self.polygon_join_threshold**2
        ):
            if len(self.polygon_points) > 2:
                self.finalize_polygon()
            return
        self.polygon_points.append(pos)
        point_diameter = self.point_radius * 2
        point_color = QColor(Qt.GlobalColor.blue)
        point_color.setAlpha(150)
        dot = QGraphicsEllipseItem(
            pos.x() - self.point_radius,
            pos.y() - self.point_radius,
            point_diameter,
            point_diameter,
        )
        dot.setBrush(QBrush(point_color))
        dot.setPen(QPen(Qt.GlobalColor.transparent))
        self.viewer.scene().addItem(dot)
        self.polygon_preview_items.append(dot)
        self.draw_polygon_preview()

    def draw_polygon_preview(self):
        for item in self.polygon_preview_items:
            if not isinstance(item, QGraphicsEllipseItem):
                if item.scene():
                    self.viewer.scene().removeItem(item)
        self.polygon_preview_items = [
            item
            for item in self.polygon_preview_items
            if isinstance(item, QGraphicsEllipseItem)
        ]
        if len(self.polygon_points) > 2:
            preview_poly = QGraphicsPolygonItem(QPolygonF(self.polygon_points))
            preview_poly.setBrush(QBrush(QColor(0, 255, 255, 100)))
            preview_poly.setPen(QPen(Qt.GlobalColor.transparent))
            self.viewer.scene().addItem(preview_poly)
            self.polygon_preview_items.append(preview_poly)

        if len(self.polygon_points) > 1:
            line_color = QColor(Qt.GlobalColor.cyan)
            line_color.setAlpha(150)
            for i in range(len(self.polygon_points) - 1):
                line = QGraphicsLineItem(
                    self.polygon_points[i].x(),
                    self.polygon_points[i].y(),
                    self.polygon_points[i + 1].x(),
                    self.polygon_points[i + 1].y(),
                )
                line.setPen(QPen(line_color, self.line_thickness))
                self.viewer.scene().addItem(line)
                self.polygon_preview_items.append(line)


def main():
    app = QApplication(sys.argv)
    qdarktheme.setup_theme()
    sam_model = SamModel(model_type="vit_h")
    main_win = MainWindow(sam_model)
    main_win.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
