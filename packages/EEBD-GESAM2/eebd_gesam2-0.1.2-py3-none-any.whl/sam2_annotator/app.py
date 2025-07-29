# src/sam2_annotator/app.py
#
# 注意：此文件只定义核心的GUI应用类 `InteractiveSAM2Annotator`。
# 程序的启动入口、路径处理和模型下载等逻辑已移至 `main.py` 文件中。
#

import sys
import os
import json
import glob
import torch
import numpy as np
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageTk
import cv2
import time
import traceback
import colorsys

# --- 处理核心的 sam2 依赖 ---
# 这个 try-except 块是正确的，应当保留。
# 它假定用户已经按照 README 的指示通过 pip install git+... 安装了 sam2。
# 如果没有安装，它会给出友好提示。
try:
    from sam2.build_sam import build_sam2
    from sam2.sam2_image_predictor import SAM2ImagePredictor
    print("成功导入SAM2组件")
except ImportError as e:
    print(f"导入SAM2组件失败: {e}", file=sys.stderr)
    print("错误：无法导入 'sam2' 库。请确保您已按照README.md中的第一步，通过以下命令安装了它：", file=sys.stderr)
    print("pip install git+https://github.com/facebookresearch/segment-anything-2.git", file=sys.stderr)
    sys.exit(1)

DEFAULT_LABELS = ["_background_", "Cropland", "Forest", "Grass", "Shrub", "Wetland", "Water", "Tundra",
                  "Impervious surface", "Bareland", "Ice/snow", "desert"]


class InteractiveSAM2Annotator(tk.Tk):
    #
    # 从这里开始，是你提供的完整的、未经修改的 InteractiveSAM2Annotator 类的代码。
    # 我们不需要对类内部的逻辑做任何修改，因为它通过 __init__ 接收所有必要的路径，
    # 这使得它具有很好的可移植性。
    #
    def __init__(self, model_path, config_path=None, device=None, output_dir="./annotations", image_dir=None):
        super().__init__()
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu") if device is None else device
        print(f"使用设备: {self.device}")

        # ... [此处省略你原来提供的 InteractiveSAM2Annotator 类的所有代码] ...
        # ... [你只需要将你最开始的那个大脚本中，从 class InteractiveSAM2Annotator(tk.Tk): 开始] ...
        # ... [到最后一个方法结束的全部内容，原封不动地复制到这里] ...
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
        self.last_session_file = os.path.join(self.output_dir, "last_session_state.json")

        self.dataset_dir = os.path.join(output_dir, "datasets")
        self.jpgs_path = os.path.join(self.dataset_dir, "JPEGImages")
        self.jsons_path = os.path.join(self.dataset_dir, "before")
        self.pngs_path = os.path.join(self.dataset_dir, "SegmentationClass")
        os.makedirs(self.jpgs_path, exist_ok=True)
        os.makedirs(self.jsons_path, exist_ok=True)
        os.makedirs(self.pngs_path, exist_ok=True)

        self.load_model(model_path, config_path)

        self.image_paths = []
        self.current_image_index = -1
        self.image_np = None
        self.image_name = ""
        self.image_list_loaded = False
        self.display_img = None
        self.current_loaded_image_dir = None

        self.points = []
        self.labels = []
        self.masks = None
        self.scores = None
        self.current_mask_idx = 0
        self.selected_mask = None
        self.current_label = DEFAULT_LABELS[0]
        self.available_labels = DEFAULT_LABELS.copy()

        self.is_polygon_mode = False
        self.polygon_points = []
        self.temp_polygon_line = None
        self.polygon_lines = []
        self.closed_polygon = False

        self.annotation_complete = False
        self.is_modified = False
        self.annotation_masks = {}
        self.history = []
        self.previous_annotations = {}

        self.colors = self.generate_colors(len(DEFAULT_LABELS))

        self.zoom_factor = 1.0
        self.min_zoom = 0.1
        self.max_zoom = 10.0
        self.pan_offset_x = 0
        self.pan_offset_y = 0
        self.pan_step = 100

        self.editable_regions = []
        self.hovered_region_index = None
        self.selected_region_index = None

        self.init_ui()

        if image_dir and os.path.exists(image_dir):
            self._initial_image_load(image_dir)
        else:
            self.status_var.set("请加载图像或提供有效的初始图像目录")

        self.protocol("WM_DELETE_WINDOW", self.on_closing)

    def _initial_image_load(self, folder_path):
        """Loads images on startup if a directory is provided."""
        self.current_loaded_image_dir = os.path.abspath(folder_path)  # Store absolute path
        start_idx = self._get_start_index_for_dir(self.current_loaded_image_dir)
        self._execute_load_procedure(self.current_loaded_image_dir, start_idx)

    def handle_load_button_press_ui(self):
        """Handles the 'Load Images' button click."""
        folder = filedialog.askdirectory(title="选择图像文件夹")
        if folder:
            abs_folder = os.path.abspath(folder)
            self.current_loaded_image_dir = abs_folder  # Update context
            start_idx = self._get_start_index_for_dir(abs_folder)  # Check session for this new/selected folder
            self._execute_load_procedure(abs_folder, start_idx)
        elif not self.image_list_loaded:  # Only update status if nothing is loaded
            self.status_var.set("请加载图像")

    def _execute_load_procedure(self, folder_path, requested_start_index):
        """Core logic to load images and jump to the correct one."""
        supported_extensions = ['*.jpg', '*.jpeg', '*.png', '*.tif', '*.tiff']
        self.image_paths = []
        for ext in supported_extensions:
            self.image_paths.extend(glob.glob(os.path.join(folder_path, ext)))
            self.image_paths.extend(glob.glob(os.path.join(folder_path, ext.upper())))
        self.image_paths.sort()  # Ensure consistent order

        if not self.image_paths:
            messagebox.showwarning("警告", f"在目录 '{folder_path}' 中未找到支持的图像文件")
            self.image_list_loaded = False
            self.current_image_index = -1
            self.image_name = ""
            self.image_canvas.delete("all")
            self.status_var.set(f"在 '{folder_path}' 中未找到图像。请加载其他图像目录。")
            self.title("SAM2 交互式图像标注工具 - 无图像")
            self.image_selector['values'] = []
            self.image_selection_var.set("")
            return False

        image_basenames = [os.path.basename(p) for p in self.image_paths]
        self.image_selector['values'] = image_basenames

        self.image_list_loaded = True
        self.current_loaded_image_dir = folder_path  # Confirm success

        if 0 <= requested_start_index < len(self.image_paths):
            self.current_image_index = requested_start_index
        else:
            self.current_image_index = -1

        if self.current_image_index == -1:
            self.next_image()
        else:
            self.load_current_image()
            self._save_last_session_info()

        return True

    def _get_start_index_for_dir(self, target_dir):
        """Checks the session file for a matching directory and returns its last index."""
        target_dir_abs = os.path.abspath(target_dir)
        if os.path.exists(self.last_session_file):
            try:
                with open(self.last_session_file, 'r') as f:
                    data = json.load(f)
                saved_dir_abs = os.path.abspath(data.get("last_image_dir", ""))
                if saved_dir_abs == target_dir_abs:
                    last_idx = data.get('last_image_index', -1)
                    print(f"加载上次会话信息: 目录 '{target_dir_abs}', 索引 {last_idx}")
                    return last_idx
            except Exception as e:
                print(f"加载上次会话文件 '{self.last_session_file}' 失败: {e}")
        print(f"未找到目录 '{target_dir_abs}' 的上次会话信息。")
        return -1

    def _save_last_session_info(self):
        """Saves the current image index for the current_loaded_image_dir."""
        if self.image_list_loaded and self.current_image_index >= 0 and self.current_loaded_image_dir:
            data = {
                "last_image_dir": os.path.abspath(self.current_loaded_image_dir),
                "last_image_index": self.current_image_index
            }
            try:
                with open(self.last_session_file, 'w') as f:
                    json.dump(data, f, indent=4)
            except Exception as e:
                print(f"保存会话文件 '{self.last_session_file}' 失败: {e}")

    def on_closing(self):
        if self.is_modified and self.image_list_loaded:
            if messagebox.askyesno("退出", "有未保存的更改，确定要退出吗？"):
                self._save_last_session_info()
                self.destroy()
            else:
                return
        else:
            self._save_last_session_info()
            self.destroy()

    def generate_colors(self, n):
        colors = []
        for i in range(n):
            hue = i / n
            saturation = 0.9
            value = 0.9
            rgb = colorsys.hsv_to_rgb(hue, saturation, value)
            rgb = tuple(int(255 * x) for x in rgb)
            colors.append(rgb)
        return colors

    def init_ui(self):
        self.title("SAM2 交互式图像标注工具")
        self.geometry("1200x800")

        main_frame = ttk.Frame(self)
        main_frame.pack(fill=tk.BOTH, expand=True)

        image_frame = ttk.Frame(main_frame)
        image_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.image_canvas = tk.Canvas(image_frame, bg="gray")
        self.image_canvas.pack(fill=tk.BOTH, expand=True)

        control_frame = ttk.Frame(main_frame, width=300)
        control_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=5, pady=5)

        self.load_button = ttk.Button(control_frame, text="加载图像", command=self.handle_load_button_press_ui)
        self.load_button.pack(fill=tk.X, pady=2)

        image_selection_frame = ttk.LabelFrame(control_frame, text="快速跳转到图像")
        image_selection_frame.pack(fill=tk.X, pady=5)
        self.image_selection_var = tk.StringVar()
        self.image_selector = ttk.Combobox(image_selection_frame, textvariable=self.image_selection_var,
                                           state="readonly")
        self.image_selector.pack(fill=tk.X, expand=True, padx=5, pady=2)
        self.image_selector.bind("<<ComboboxSelected>>", self.on_image_select)

        zoom_frame = ttk.Frame(control_frame)
        zoom_frame.pack(fill=tk.X, pady=2)
        ttk.Button(zoom_frame, text="放大", command=lambda: self.zoom(1.2)).pack(side=tk.LEFT, fill=tk.X, expand=True)
        ttk.Button(zoom_frame, text="缩小", command=lambda: self.zoom(0.8333)).pack(side=tk.LEFT, fill=tk.X,
                                                                                    expand=True)

        pan_frame = ttk.Frame(control_frame)
        pan_frame.pack(fill=tk.X, pady=2)
        pan_frame.columnconfigure((0, 1), weight=1)
        ttk.Button(pan_frame, text="向左移动", command=self.pan_left).grid(row=0, column=0, sticky="ew", padx=2)
        ttk.Button(pan_frame, text="向右移动", command=self.pan_right).grid(row=0, column=1, sticky="ew", padx=2)
        ttk.Button(pan_frame, text="向上移动", command=self.pan_up).grid(row=1, column=0, sticky="ew", padx=2)
        ttk.Button(pan_frame, text="向下移动", command=self.pan_down).grid(row=1, column=1, sticky="ew", padx=2)

        self.mode_frame = ttk.LabelFrame(control_frame, text="选择操作模式")
        self.mode_frame.pack(fill=tk.X, pady=2)
        self.mode_var = tk.StringVar(value="SAM标注")
        self.sam_mode_radio = ttk.Radiobutton(self.mode_frame, text="SAM标注", variable=self.mode_var, value="SAM标注",
                                              command=self.change_to_sam_mode)
        self.sam_mode_radio.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.polygon_mode_radio = ttk.Radiobutton(self.mode_frame, text="多边形", variable=self.mode_var,
                                                  value="多边形", command=self.change_to_polygon_mode)
        self.polygon_mode_radio.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.edit_mode_radio = ttk.Radiobutton(self.mode_frame, text="编辑标签", variable=self.mode_var,
                                               value="编辑标签", command=self.change_to_edit_mode)
        self.edit_mode_radio.pack(side=tk.LEFT, fill=tk.X, expand=True)

        self.sam_frame = ttk.LabelFrame(control_frame, text="SAM标注工具")
        self.sam_frame.pack(fill=tk.X, pady=2)
        self.predict_button = ttk.Button(self.sam_frame, text="预测掩码", command=self.predict_masks)
        self.predict_button.pack(fill=tk.X, pady=2)
        self.select_button = ttk.Button(self.sam_frame, text="选择掩码", command=self.select_mask)
        self.select_button.pack(fill=tk.X, pady=2)
        self.next_mask_button = ttk.Button(self.sam_frame, text="下一个掩码", command=self.next_mask)
        self.next_mask_button.pack(fill=tk.X, pady=2)

        self.polygon_frame = ttk.LabelFrame(control_frame, text="多边形标注工具")
        self.close_polygon_button = ttk.Button(self.polygon_frame, text="闭合多边形", command=self.close_polygon)
        self.close_polygon_button.pack(fill=tk.X, pady=2)
        self.clear_polygon_button = ttk.Button(self.polygon_frame, text="清除多边形", command=self.clear_polygon)
        self.clear_polygon_button.pack(fill=tk.X, pady=2)

        self.edit_frame = ttk.LabelFrame(control_frame, text="编辑工具")
        self.update_label_button = ttk.Button(self.edit_frame, text="更新标签", command=self.update_selected_label,
                                              state=tk.DISABLED)
        self.update_label_button.pack(fill=tk.X, pady=2)

        self.undo_button = ttk.Button(control_frame, text="撤销", command=self.undo)
        self.undo_button.pack(fill=tk.X, pady=2)
        self.reset_button = ttk.Button(control_frame, text="重置", command=self.reset_annotation)
        self.reset_button.pack(fill=tk.X, pady=2)

        label_frame = ttk.Frame(control_frame)
        label_frame.pack(fill=tk.X, pady=2)
        ttk.Label(label_frame, text="标签:").pack(side=tk.LEFT)
        self.label_var = tk.StringVar(value=self.current_label)
        self.label_combo = ttk.Combobox(label_frame, textvariable=self.label_var, values=self.available_labels)
        self.label_combo.bind("<<ComboboxSelected>>", self.on_label_change)
        self.label_combo.pack(side=tk.LEFT, fill=tk.X, expand=True)

        self.confirm_button = ttk.Button(control_frame, text="确认并锁定此区域", command=self.confirm_label)
        self.confirm_button.pack(fill=tk.X, pady=2)
        self.complete_button = ttk.Button(control_frame, text="完成并保存", command=self.complete_annotation)
        self.complete_button.pack(fill=tk.X, pady=2)

        nav_frame = ttk.Frame(control_frame)
        nav_frame.pack(fill=tk.X, pady=2)
        self.prev_button = ttk.Button(nav_frame, text="上一张", command=self.prev_image)
        self.prev_button.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.next_button = ttk.Button(nav_frame, text="下一张", command=self.next_image)
        self.next_button.pack(side=tk.LEFT, fill=tk.X, expand=True)

        self.sam_help_text = "SAM模式: 左键正向点, 右键负向点, 中键擦除。"
        self.polygon_help_text = "多边形模式: 左键添加顶点, 右键删除顶点。"
        self.edit_help_text = "编辑模式: 单击已标注区域可选中, 然后在上方选择新标签并点击'更新标签'按钮进行修改。"
        self.help_var = tk.StringVar(value=self.sam_help_text)
        self.help_label = ttk.Label(control_frame, textvariable=self.help_var, wraplength=280, justify=tk.LEFT)
        self.help_label.pack(fill=tk.X, pady=10, padx=5)

        self.status_var = tk.StringVar(value="请加载图像")
        status_bar = ttk.Label(self, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W)
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)

        self.change_to_sam_mode()

    def on_image_select(self, event=None):
        selected_image_name = self.image_selection_var.get()
        if not selected_image_name or not self.image_list_loaded or selected_image_name == self.image_name:
            return

        try:
            target_index = [os.path.basename(p) for p in self.image_paths].index(selected_image_name)
        except ValueError:
            messagebox.showerror("错误", f"在图像列表中未找到 '{selected_image_name}'")
            self.image_selection_var.set(self.image_name)
            return

        if self.is_modified:
            if not messagebox.askyesno("提示", "当前图像已修改但未保存，是否继续？"):
                self.image_selection_var.set(self.image_name)
                return

        if self.annotation_masks and self.image_name:
            self.previous_annotations[self.image_name] = self.annotation_masks.copy()

        self.current_image_index = target_index
        self.zoom_factor = 1.0
        self.pan_offset_x = 0
        self.pan_offset_y = 0
        self.load_current_image()
        self._save_last_session_info()

    def bind_sam_events(self):
        self.image_canvas.unbind("<Button-1>")
        self.image_canvas.unbind("<Button-3>")
        self.image_canvas.unbind("<Button-2>")
        self.image_canvas.unbind("<Motion>")
        self.image_canvas.bind("<Button-1>", self.on_left_click)
        self.image_canvas.bind("<Button-3>", self.on_right_click)
        self.image_canvas.bind("<Button-2>", self.on_middle_click)
        self.image_canvas.bind("<Configure>", self.on_canvas_resize)

    def bind_polygon_events(self):
        self.image_canvas.unbind("<Button-1>")
        self.image_canvas.unbind("<Button-3>")
        self.image_canvas.unbind("<Button-2>")
        self.image_canvas.unbind("<Motion>")
        self.image_canvas.bind("<Button-1>", self.on_polygon_left_click)
        self.image_canvas.bind("<Button-3>", self.on_polygon_right_click)
        self.image_canvas.bind("<Motion>", self.on_polygon_mouse_move)
        self.image_canvas.bind("<Configure>", self.on_canvas_resize)

    def bind_edit_events(self):
        self.image_canvas.unbind("<Button-1>")
        self.image_canvas.unbind("<Button-3>")
        self.image_canvas.unbind("<Button-2>")
        self.image_canvas.unbind("<Motion>")
        self.image_canvas.bind("<Motion>", self.on_edit_mode_motion)
        self.image_canvas.bind("<Button-1>", self.on_edit_mode_click)
        self.image_canvas.bind("<Configure>", self.on_canvas_resize)

    def zoom(self, scale):
        new_zoom = self.zoom_factor * scale
        if new_zoom < self.min_zoom or new_zoom > self.max_zoom:
            return
        self.zoom_factor = new_zoom
        self.status_var.set(
            f"当前图像: {self.image_name} | 缩放: {self.zoom_factor:.2f}x | 平移: ({self.pan_offset_x}, {self.pan_offset_y})")
        if self.image_np is not None:
            self.display_image(self.image_np)

    def pan_left(self):
        if self.image_np is None:
            return
        self.pan_offset_x -= self.pan_step
        self.status_var.set(
            f"当前图像: {self.image_name} | 缩放: {self.zoom_factor:.2f}x | 平移: ({self.pan_offset_x}, {self.pan_offset_y})")
        self.display_image(self.image_np)

    def pan_right(self):
        if self.image_np is None:
            return
        self.pan_offset_x += self.pan_step
        self.status_var.set(
            f"当前图像: {self.image_name} | 缩放: {self.zoom_factor:.2f}x | 平移: ({self.pan_offset_x}, {self.pan_offset_y})")
        self.display_image(self.image_np)

    def pan_up(self):
        if self.image_np is None:
            return
        self.pan_offset_y -= self.pan_step
        self.status_var.set(
            f"当前图像: {self.image_name} | 缩放: {self.zoom_factor:.2f}x | 平移: ({self.pan_offset_x}, {self.pan_offset_y})")
        self.display_image(self.image_np)

    def pan_down(self):
        if self.image_np is None:
            return
        self.pan_offset_y += self.pan_step
        self.status_var.set(
            f"当前图像: {self.image_name} | 缩放: {self.zoom_factor:.2f}x | 平移: ({self.pan_offset_x}, {self.pan_offset_y})")
        self.display_image(self.image_np)

    def change_to_sam_mode(self):
        self.sam_frame.pack(fill=tk.X, pady=2, after=self.mode_frame)
        self.polygon_frame.pack_forget()
        self.edit_frame.pack_forget()
        self.confirm_button.config(state=tk.NORMAL)

        self.help_var.set(self.sam_help_text)
        self.bind_sam_events()
        self.clear_polygon()
        self._clear_selection_state()
        if self.image_np is not None:
            self.display_image(self.image_np)

    def change_to_polygon_mode(self):
        self.is_polygon_mode = True
        self.sam_frame.pack_forget()
        self.polygon_frame.pack(fill=tk.X, pady=2, after=self.mode_frame)
        self.edit_frame.pack_forget()
        self.confirm_button.config(state=tk.NORMAL)

        self.help_var.set(self.polygon_help_text)
        self.bind_polygon_events()
        self._clear_selection_state()
        if self.image_np is not None:
            self.display_image(self.image_np)

    def change_to_edit_mode(self):
        self.sam_frame.pack_forget()
        self.polygon_frame.pack_forget()
        self.edit_frame.pack(fill=tk.X, pady=2, after=self.mode_frame)
        self.confirm_button.config(state=tk.DISABLED)

        self.help_var.set(self.edit_help_text)
        self.bind_edit_events()
        self.clear_polygon()
        self._prepare_for_editing()
        if self.image_np is not None:
            self.display_image(self.image_np)

    def on_polygon_left_click(self, event):
        if self.image_np is None or self.closed_polygon:
            return

        x, y = self._convert_canvas_to_image_coords(event.x, event.y)
        canvas_x = event.x
        canvas_y = event.y

        if len(self.polygon_points) > 2:
            first_x, first_y = self.polygon_points[0]
            canvas_first_x, canvas_first_y = self._convert_image_to_canvas_coords(first_x, first_y)
            if ((canvas_x - canvas_first_x) ** 2 + (canvas_y - canvas_first_y) ** 2) ** 0.5 < 10:
                self.close_polygon()
                return

        self.polygon_points.append((x, y))
        point_id = self.image_canvas.create_oval(
            canvas_x - 5, canvas_y - 5, canvas_x + 5, canvas_y + 5,
            fill="red", outline="white", tags="polygon_point"
        )

        if len(self.polygon_points) > 1:
            prev_x, prev_y = self._convert_image_to_canvas_coords(
                self.polygon_points[-2][0], self.polygon_points[-2][1]
            )
            line_id = self.image_canvas.create_line(
                prev_x, prev_y, canvas_x, canvas_y,
                fill="yellow", width=2, tags="polygon_line"
            )
            self.polygon_lines.append(line_id)

        self.status_var.set(f"多边形顶点 #{len(self.polygon_points)} 添加在 ({x}, {y})")

    def on_polygon_right_click(self, event):
        if not self.polygon_points or self.closed_polygon:
            return

        self.polygon_points.pop()
        points = self.image_canvas.find_withtag("polygon_point")
        if points:
            self.image_canvas.delete(points[-1])

        if self.polygon_lines:
            self.image_canvas.delete(self.polygon_lines.pop())

        if self.polygon_points and self.temp_polygon_line:
            prev_x, prev_y = self._convert_image_to_canvas_coords(
                self.polygon_points[-1][0], self.polygon_points[-1][1]
            )
            self.image_canvas.coords(
                self.temp_polygon_line,
                prev_x, prev_y, event.x, event.y
            )

        self.status_var.set(f"已删除多边形最后一个顶点，剩余 {len(self.polygon_points)} 个顶点")

    def on_polygon_mouse_move(self, event):
        if not self.polygon_points or self.closed_polygon:
            return

        last_x, last_y = self._convert_image_to_canvas_coords(
            self.polygon_points[-1][0], self.polygon_points[-1][1]
        )

        if self.temp_polygon_line:
            self.image_canvas.coords(
                self.temp_polygon_line,
                last_x, last_y, event.x, event.y
            )
        else:
            self.temp_polygon_line = self.image_canvas.create_line(
                last_x, last_y, event.x, event.y,
                fill="gray", dash=(4, 4), tags="temp_line"
            )

    def clear_polygon(self):
        self.polygon_points = []
        self.closed_polygon = False
        self.image_canvas.delete("polygon_point")
        self.image_canvas.delete("polygon_line")
        self.image_canvas.delete("temp_line")
        self.temp_polygon_line = None
        self.polygon_lines = []
        self.selected_mask = None
        self.status_var.set("已清除多边形")
        if self.image_np is not None:
            self.display_image(self.image_np)

    def close_polygon(self):
        if len(self.polygon_points) < 3:
            messagebox.showwarning("警告", "多边形至少需要3个顶点")
            return

        self.save_to_history()
        self.closed_polygon = True

        first_x, first_y = self._convert_image_to_canvas_coords(
            self.polygon_points[0][0], self.polygon_points[0][1]
        )
        last_x, last_y = self._convert_image_to_canvas_coords(
            self.polygon_points[-1][0], self.polygon_points[-1][1]
        )
        line_id = self.image_canvas.create_line(
            last_x, last_y, first_x, first_y,
            fill="yellow", width=2, tags="polygon_line"
        )
        self.polygon_lines.append(line_id)

        mask = np.zeros(self.image_np.shape[:2], dtype=np.uint8)
        pts = np.array(self.polygon_points, dtype=np.int32)
        cv2.fillPoly(mask, [pts], 1)
        mask_bool = mask.astype(bool)

        locked_mask = self._get_locked_mask()
        if locked_mask is not None:
            original_area = np.sum(mask_bool)
            mask_bool = np.logical_and(mask_bool, ~locked_mask)
            new_area = np.sum(mask_bool)
            if original_area > 0 and new_area == 0:
                messagebox.showwarning("警告", "您绘制的多边形完全位于已标注区域内，无有效新区域。")
                self.clear_polygon()
                self.display_image(self.image_np)
                return

        self.selected_mask = mask_bool
        self.is_modified = True

        self.image_canvas.delete("polygon_point")
        self.image_canvas.delete("polygon_line")
        self.image_canvas.delete("temp_line")
        self.temp_polygon_line = None
        self.polygon_lines = []

        self.display_image(self.image_np)
        self.status_var.set("多边形已闭合，请分配标签")

    def on_canvas_resize(self, event):
        if self.image_np is not None:
            self.display_image(self.image_np)

    def load_model(self, model_path, config_path=None):
        try:
            print(f"正在加载SAM2模型: {model_path}")
            if not os.path.exists(model_path):
                raise FileNotFoundError(f"模型文件不存在: {model_path}")
            if config_path is None:
                config_path = "configs/sam2/sam2_hiera_l.yaml" if "large" in str(model_path).lower() else "configs/sam2/sam2_hiera_b.yaml"
                print(f"未提供配置路径，使用: {config_path}")
            self.model = build_sam2(config_path, model_path, device=self.device)
            print("模型加载成功")
        except Exception as e:
            print(f"加载模型失败: {e}")
            traceback.print_exc()
            messagebox.showerror("模型加载失败", f"无法加载SAM2模型: {e}\n请检查模型和配置文件路径是否正确。")
            self.destroy() # 关键：如果模型加载失败，直接关闭应用

    def next_image(self):
        if not self.image_list_loaded or not self.image_paths:
            messagebox.showwarning("警告", "未加载图像列表")
            return
        if self.is_modified:
            if not messagebox.askyesno("提示", "当前图像已修改但未保存，是否继续？"):
                return
        if self.current_image_index < len(self.image_paths) - 1:
            if self.annotation_masks and self.image_name:
                self.previous_annotations[self.image_name] = self.annotation_masks.copy()
            self.current_image_index += 1
            self.zoom_factor = 1.0
            self.pan_offset_x = 0
            self.pan_offset_y = 0
            self.load_current_image()
            self._save_last_session_info()
        else:
            messagebox.showinfo("提示", "已经是最后一张图像")

    def prev_image(self):
        if not self.image_list_loaded or not self.image_paths:
            messagebox.showwarning("警告", "未加载图像列表")
            return
        if self.is_modified:
            if not messagebox.askyesno("提示", "当前图像已修改但未保存，是否继续？"):
                return
        if self.current_image_index > 0:
            if self.annotation_masks and self.image_name:
                self.previous_annotations[self.image_name] = self.annotation_masks.copy()
            self.current_image_index -= 1
            self.zoom_factor = 1.0
            self.pan_offset_x = 0
            self.pan_offset_y = 0
            self.load_current_image()
            self._save_last_session_info()
        else:
            messagebox.showinfo("提示", "已经是第一张图像")

    def load_current_image(self):
        if not (0 <= self.current_image_index < len(self.image_paths)):
            print(f"错误: current_image_index ({self.current_image_index}) 超出范围 (0-{len(self.image_paths) - 1})")
            self.status_var.set("错误：图像索引超出范围")
            self.title("SAM2 交互式图像标注工具 - 索引错误")
            if self.image_np is not None:
                self.image_np = None
                self.image_canvas.delete("all")
            return

        image_path = self.image_paths[self.current_image_index]
        try:
            image = Image.open(image_path)
            self.image_np = np.array(image.convert("RGB"))
            self.image_name = os.path.basename(image_path)

            self.title(f"SAM2 交互式图像标注工具 - {self.image_name}")

            if self.image_list_loaded:
                self.image_selection_var.set(self.image_name)

            self.reset_annotation()
            self.predictor = SAM2ImagePredictor(self.model)
            self.predictor.set_image(self.image_np)

            self.annotation_masks = {}
            json_file = os.path.join(self.jsons_path, self.image_name.rsplit('.', 1)[0] + '.json')

            if self.image_name in self.previous_annotations:
                self.annotation_masks = self.previous_annotations[self.image_name].copy()
            elif os.path.exists(json_file):
                with open(json_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                for shape in data.get('shapes', []):
                    label = shape['label']
                    points = np.array(shape['points'], dtype=np.int32)
                    if points.ndim == 2 and points.shape[0] >= 3 and points.shape[1] == 2:
                        mask = np.zeros(self.image_np.shape[:2], dtype=np.uint8)
                        cv2.fillPoly(mask, [points], 1)
                        mask_bool = mask.astype(bool)
                        if label not in self.annotation_masks:
                            self.annotation_masks[label] = []
                        self.annotation_masks[label].append(mask_bool)
                    else:
                        print(f"警告: 在JSON文件 '{json_file}' 中找到标签 '{label}' 的无效点集。")

            self.status_var.set(
                f"当前图像: {self.image_name} | 进度: {self.current_image_index + 1}/{len(self.image_paths)} | 缩放: {self.zoom_factor:.2f}x | 平移: ({self.pan_offset_x}, {self.pan_offset_y})")

            current_mode = self.mode_var.get()
            if current_mode == "SAM标注":
                self.change_to_sam_mode()
            elif current_mode == "多边形":
                self.change_to_polygon_mode()
            elif current_mode == "编辑标签":
                self.change_to_edit_mode()

            self.display_image(self.image_np)

        except FileNotFoundError:
            print(f"错误: 图像文件未找到 '{image_path}'")
            messagebox.showerror("错误", f"图像文件未找到: {os.path.basename(image_path)}")
            self.status_var.set(f"错误: 图像文件 '{os.path.basename(image_path)}' 未找到。")
            self.title(f"SAM2 交互式图像标注工具 - 文件未找到")
            if len(self.image_paths) > 1:
                self.image_paths.pop(self.current_image_index)
                image_basenames = [os.path.basename(p) for p in self.image_paths]
                self.image_selector['values'] = image_basenames
                if self.current_image_index >= len(self.image_paths) and len(self.image_paths) > 0:
                    self.current_image_index = len(self.image_paths) - 1
                elif len(self.image_paths) == 0:
                    self.current_image_index = -1
                    self.image_list_loaded = False
                    self.title("SAM2 交互式图像标注工具 - 无图像")
                    self.image_canvas.delete("all")
                    self.status_var.set("所有图像加载失败或列表为空。")
                    return
                self.load_current_image()
            else:
                self.image_np = None
                self.image_name = ""
                self.image_list_loaded = False
                self.current_image_index = -1
                self.image_canvas.delete("all")
                self.status_var.set(f"图像 '{os.path.basename(image_path)}' 未找到。列表为空。")
                self.image_selector['values'] = []
                self.image_selection_var.set("")
        except Exception as e:
            print(f"加载图像 '{image_path}' 失败: {e}")
            traceback.print_exc()
            messagebox.showerror("错误", f"加载图像 '{os.path.basename(image_path)}' 失败: {str(e)}")
            self.status_var.set(f"加载图像 '{os.path.basename(image_path)}' 失败。")
            self.title(f"SAM2 交互式图像标注工具 - 加载失败")

    def display_image(self, image):
        self.display_img = image.copy()

        for label, masks in self.annotation_masks.items():
            if label in self.available_labels:
                label_idx = self.available_labels.index(label)
            else:
                self.available_labels.append(label)
                self.label_combo['values'] = self.available_labels
                label_idx = len(self.available_labels) - 1
                if label_idx >= len(self.colors):
                    self.colors = self.generate_colors(len(self.available_labels))

            color = self.colors[label_idx % len(self.colors)]
            combined_mask = np.zeros_like(masks[0], dtype=bool) if masks else None

            for i, mask in enumerate(masks):
                alpha = 0.4
                self.apply_mask(self.display_img, mask, color, alpha=alpha)
                if combined_mask is not None:
                    combined_mask = np.logical_or(combined_mask, mask)

            if combined_mask is not None and np.any(combined_mask):
                y_indices, x_indices = np.where(combined_mask)
                if len(y_indices) > 0 and len(x_indices) > 0:
                    center_y = int(np.mean(y_indices))
                    center_x = int(np.mean(x_indices))
                    text_x = max(0, min(center_x, self.display_img.shape[1] - 10))
                    text_y = max(15, min(center_y, self.display_img.shape[0] - 5))
                    cv2.putText(self.display_img, label, (text_x, text_y),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)

        def draw_mask_contours(mask_to_draw, color=(0, 165, 255), alpha=0.5):
            if mask_to_draw is None or not np.any(mask_to_draw):
                return
            self.apply_mask(self.display_img, mask_to_draw, color, alpha)
            contours, _ = cv2.findContours(
                mask_to_draw.astype(np.uint8),
                cv2.RETR_EXTERNAL,
                cv2.CHAIN_APPROX_SIMPLE
            )
            cv2.drawContours(self.display_img, contours, -1, (255, 255, 255), 1)

        if self.masks is not None and len(self.masks) > 0 and self.current_mask_idx < len(self.masks):
            mask = self.masks[self.current_mask_idx]
            draw_mask_contours(mask)

        if self.selected_mask is not None:
            draw_mask_contours(self.selected_mask)

        if self.mode_var.get() == "SAM标注":
            self.draw_points(self.display_img)

        if self.mode_var.get() == "编辑标签":
            for i, region in enumerate(self.editable_regions):
                x, y, w, h = region['bbox']
                color = (255, 255, 255)
                if i == self.selected_region_index:
                    color = (0, 255, 0)
                elif i == self.hovered_region_index:
                    color = (255, 255, 0)
                cv2.rectangle(self.display_img, (x, y), (x + w, y + h), color, 2)

        canvas_width = self.image_canvas.winfo_width()
        canvas_height = self.image_canvas.winfo_height()
        img_height, img_width = self.display_img.shape[:2]

        if canvas_width <= 1 or canvas_height <= 1:
            canvas_width = max(1, self.image_canvas.winfo_reqwidth())
            canvas_height = max(1, self.image_canvas.winfo_reqheight())
            if canvas_width <= 1: canvas_width = 800
            if canvas_height <= 1: canvas_height = 600

        zoomed_width = int(img_width * self.zoom_factor)
        zoomed_height = int(img_height * self.zoom_factor)

        if zoomed_width < 1 or zoomed_height < 1:
            zoomed_width = max(1, zoomed_width)
            zoomed_height = max(1, zoomed_height)

        image_at_zoom_level = cv2.resize(self.display_img, (zoomed_width, zoomed_height), interpolation=cv2.INTER_AREA)

        image_pil = Image.fromarray(image_at_zoom_level)
        self.photo = ImageTk.PhotoImage(image_pil)
        self.image_canvas.delete("all")

        center_x = canvas_width // 2
        center_y = canvas_height // 2
        draw_x = center_x - zoomed_width // 2 + self.pan_offset_x
        draw_y = center_y - zoomed_height // 2 + self.pan_offset_y

        self.image_canvas.create_image(
            draw_x, draw_y,
            image=self.photo,
            anchor="nw"
        )

        self.current_display_scale = self.zoom_factor
        self.canvas_offset_x = draw_x
        self.canvas_offset_y = draw_y

        if self.mode_var.get() == "多边形" and self.polygon_points:
            self.redraw_polygon()

    def redraw_polygon(self):
        self.image_canvas.delete("polygon_point")
        self.image_canvas.delete("polygon_line")
        self.image_canvas.delete("temp_line")
        self.polygon_lines = []
        self.temp_polygon_line = None

        for i, (x, y) in enumerate(self.polygon_points):
            canvas_x, canvas_y = self._convert_image_to_canvas_coords(x, y)
            self.image_canvas.create_oval(
                canvas_x - 5, canvas_y - 5, canvas_x + 5, canvas_y + 5,
                fill="red", outline="white", tags="polygon_point"
            )
            if i > 0:
                prev_x_img, prev_y_img = self.polygon_points[i - 1]
                prev_x_canvas, prev_y_canvas = self._convert_image_to_canvas_coords(prev_x_img, prev_y_img)
                line_id = self.image_canvas.create_line(
                    prev_x_canvas, prev_y_canvas, canvas_x, canvas_y,
                    fill="yellow", width=2, tags="polygon_line"
                )
                self.polygon_lines.append(line_id)

        if self.closed_polygon and len(self.polygon_points) > 2:
            first_x_img, first_y_img = self.polygon_points[0]
            last_x_img, last_y_img = self.polygon_points[-1]
            first_x_canvas, first_y_canvas = self._convert_image_to_canvas_coords(first_x_img, first_y_img)
            last_x_canvas, last_y_canvas = self._convert_image_to_canvas_coords(last_x_img, last_y_img)

            line_id = self.image_canvas.create_line(
                last_x_canvas, last_y_canvas, first_x_canvas, first_y_canvas,
                fill="yellow", width=2, tags="polygon_line"
            )
            self.polygon_lines.append(line_id)

    def apply_mask(self, image, mask, color, alpha=0.5):
        mask = mask.astype(bool)
        colored_mask = np.zeros_like(image)
        colored_mask[mask] = color
        cv2.addWeighted(colored_mask, alpha, image, 1.0, 0, image)
        return image

    def draw_points(self, image_to_draw_on):
        if self.image_np is None: return

        for i, (point_orig_coords, label) in enumerate(zip(self.points, self.labels)):
            y_orig, x_orig = point_orig_coords
            color = (0, 255, 0) if label == 1 else (0, 0, 255)
            star_base_size = 10
            star_points = []
            for j in range(10):
                angle = np.pi / 5 * j - np.pi / 2
                radius = star_base_size if j % 2 == 0 else star_base_size * 0.4
                point_x = int(x_orig + radius * np.cos(angle))
                point_y = int(y_orig + radius * np.sin(angle))
                star_points.append([point_x, point_y])

            star_points_np = np.array(star_points, dtype=np.int32).reshape((-1, 1, 2))
            cv2.polylines(image_to_draw_on, [star_points_np], True, (255, 255, 255), 2)
            cv2.fillPoly(image_to_draw_on, [star_points_np], color)

    def _convert_canvas_to_image_coords(self, canvas_x, canvas_y):
        if self.image_np is None or self.current_display_scale == 0:
            return canvas_x, canvas_y

        x_on_zoomed_image = canvas_x - self.canvas_offset_x
        y_on_zoomed_image = canvas_y - self.canvas_offset_y

        original_x = x_on_zoomed_image / self.current_display_scale
        original_y = y_on_zoomed_image / self.current_display_scale

        img_height, img_width = self.image_np.shape[:2]
        original_x = max(0, min(original_x, img_width - 1))
        original_y = max(0, min(original_y, img_height - 1))

        return int(original_x), int(original_y)

    def _convert_image_to_canvas_coords(self, image_x, image_y):
        if self.image_np is None:
            return image_x, image_y

        x_on_zoomed_image = image_x * self.current_display_scale
        y_on_zoomed_image = image_y * self.current_display_scale

        canvas_x = x_on_zoomed_image + self.canvas_offset_x
        canvas_y = y_on_zoomed_image + self.canvas_offset_y

        return int(canvas_x), int(canvas_y)

    def on_left_click(self, event):
        if self.image_np is None: return
        x, y = self._convert_canvas_to_image_coords(event.x, event.y)
        self.add_point(x, y, is_positive=True)
        self.display_image(self.image_np)

    def on_right_click(self, event):
        if self.image_np is None: return
        x, y = self._convert_canvas_to_image_coords(event.x, event.y)
        self.add_point(x, y, is_positive=False)
        self.display_image(self.image_np)

    def on_middle_click(self, event):
        if self.image_np is None: return
        x, y = self._convert_canvas_to_image_coords(event.x, event.y)
        self.remove_mask_region(x, y)
        self.display_image(self.image_np)

    def on_edit_mode_motion(self, event):
        if self.image_np is None: return
        x, y = self._convert_canvas_to_image_coords(event.x, event.y)

        current_hover = None
        for i, region in enumerate(self.editable_regions):
            rx, ry, rw, rh = region['bbox']
            if rx <= x < rx + rw and ry <= y < ry + rh:
                current_hover = i
                break

        if current_hover != self.hovered_region_index:
            self.hovered_region_index = current_hover
            self.display_image(self.image_np)

    def on_edit_mode_click(self, event):
        if self.hovered_region_index is not None:
            self.selected_region_index = self.hovered_region_index
            selected_label = self.editable_regions[self.selected_region_index]['label']
            self.label_var.set(selected_label)
            self.update_label_button.config(state=tk.NORMAL)
            self.status_var.set(f"已选中区域，标签为 '{selected_label}'。可选择新标签并点击'更新标签'。")
        else:
            self._clear_selection_state()
            self.status_var.set("已取消选择。")

        self.display_image(self.image_np)

    def remove_mask_region(self, x, y, radius=20):
        modified = False
        if self.image_np is None: return False

        erase_mask = np.zeros(self.image_np.shape[:2], dtype=np.uint8)
        cv2.circle(erase_mask, (x, y), radius, 1, -1)
        erase_mask_bool = erase_mask.astype(bool)

        if self.masks is not None and self.current_mask_idx < len(self.masks) and \
                self.masks[self.current_mask_idx] is not None:
            current_pred_mask = self.masks[self.current_mask_idx]
            if np.any(current_pred_mask[erase_mask_bool]):
                self.save_to_history()
                self.masks[self.current_mask_idx] = np.logical_and(current_pred_mask, ~erase_mask_bool)
                self.is_modified = True
                modified = True
                self.status_var.set(f"已从预测掩码中移除区域")

        if not modified and self.selected_mask is not None:
            if np.any(self.selected_mask[erase_mask_bool]):
                self.save_to_history()
                self.selected_mask = np.logical_and(self.selected_mask, ~erase_mask_bool)
                self.is_modified = True
                modified = True
                self.status_var.set(f"已从选中掩码中移除区域")

        if not modified:
            for label, masks_list in self.annotation_masks.items():
                for i, mask in enumerate(masks_list):
                    if np.any(mask[erase_mask_bool]):
                        self.save_to_history()
                        self.annotation_masks[label][i] = np.logical_and(mask, ~erase_mask_bool)
                        self.is_modified = True
                        modified = True
                        self.status_var.set(f"已从标签 '{label}' 的掩码中移除区域")
                        break
                if modified:
                    break

        if not modified:
            self.status_var.set("点击位置没有可擦除的掩码")
        else:
            self.display_image(self.image_np)
        return modified

    def reset_annotation(self):
        self.points = []
        self.labels = []
        self.masks = None
        self.scores = None
        self.current_mask_idx = 0
        self.selected_mask = None
        self.annotation_complete = False
        self.is_modified = False
        self.history = []

        self.clear_polygon()
        self._clear_selection_state()

        if self.image_np is not None:
            current_mode = self.mode_var.get()
            if current_mode == "编辑标签":
                self._prepare_for_editing()
            self.display_image(self.image_np)

    def save_to_history(self):
        state = {
            'points': self.points.copy(),
            'labels': self.labels.copy(),
            'masks': self.masks.copy() if self.masks is not None else None,
            'scores': self.scores.copy() if self.scores is not None else None,
            'current_mask_idx': self.current_mask_idx,
            'selected_mask': self.selected_mask.copy() if self.selected_mask is not None else None,
            'annotation_masks': {k: [m.copy() for m in v] for k, v in self.annotation_masks.items()},
            'is_modified': self.is_modified,
            'polygon_points': self.polygon_points.copy(),
            'closed_polygon': self.closed_polygon,
        }
        self.history.append(state)

    def undo(self):
        if not self.history:
            messagebox.showinfo("提示", "没有可撤销的操作")
            return
        state = self.history.pop()
        self.points = state['points']
        self.labels = state['labels']
        self.masks = state['masks']
        self.scores = state['scores']
        self.current_mask_idx = state['current_mask_idx']
        self.selected_mask = state['selected_mask']
        self.annotation_masks = state['annotation_masks']
        self.is_modified = state['is_modified']
        self.polygon_points = state['polygon_points']
        self.closed_polygon = state['closed_polygon']

        if self.image_np is not None:
            if self.mode_var.get() == "编辑标签":
                self._prepare_for_editing()
                self._clear_selection_state()
            self.display_image(self.image_np)
            if self.is_polygon_mode:
                self.redraw_polygon()
        messagebox.showinfo("提示", "已撤销上一步操作")

    def add_point(self, x, y, is_positive=True):
        self.save_to_history()
        label = 1 if is_positive else 0
        self.points.append([y, x])
        self.labels.append(label)
        self.is_modified = True
        point_type = "正向" if is_positive else "负向"
        self.status_var.set(f"添加{point_type}点: ({x}, {y}), 总点数: {len(self.points)}")
        return len(self.points)

    def _get_locked_mask(self):
        if not self.annotation_masks or self.image_np is None:
            return None
        h, w = self.image_np.shape[:2]
        locked_mask = np.zeros((h, w), dtype=bool)
        for _, masks_list in self.annotation_masks.items():
            for mask in masks_list:
                locked_mask = np.logical_or(locked_mask, mask)
        return locked_mask

    def predict_masks(self):
        if self.image_np is None:
            messagebox.showwarning("警告", "未加载图像")
            return
        if len(self.points) == 0:
            messagebox.showwarning("警告", "请先添加至少一个点")
            return

        locked_mask = self._get_locked_mask()

        points_for_sam = np.array([[p[1], p[0]] for p in self.points])
        labels_array = np.array(self.labels)

        start_time = time.time()
        try:
            masks, scores, logits = self.predictor.predict(
                point_coords=points_for_sam,
                point_labels=labels_array,
                multimask_output=True
            )
        except Exception as e:
            print(f"掩码预测失败: {e}")
            traceback.print_exc()
            messagebox.showerror("错误", f"掩码预测失败: {str(e)}")
            return
        end_time = time.time()

        if locked_mask is not None:
            unlocked_area = ~locked_mask
            masks = [np.logical_and(m, unlocked_area) for m in masks]

        valid_masks = []
        valid_scores = []
        for mask, score in zip(masks, scores):
            if np.any(mask):
                valid_masks.append(mask)
                valid_scores.append(score)

        if not valid_masks:
            messagebox.showwarning("警告", "预测的掩码均为空或完全位于已标注区域，请尝试在未标注区域调整点击位置。")
            self.masks = None
            self.scores = None
            self.current_mask_idx = 0
            if self.image_np is not None: self.display_image(self.image_np)
            return

        sorted_ind = np.argsort(valid_scores)[::-1]
        self.masks = np.array(valid_masks)[sorted_ind][:3]
        self.scores = np.array(valid_scores)[sorted_ind][:3]
        self.current_mask_idx = 0
        self.is_modified = True
        self.save_to_history()
        messagebox.showinfo("提示", f"预测完成，用时 {end_time - start_time:.2f}秒，找到 {len(self.masks)} 个有效新掩码")
        if self.image_np is not None: self.display_image(self.image_np)

    def next_mask(self):
        if self.masks is None or len(self.masks) <= 1:
            messagebox.showinfo("提示", "没有更多掩码可用")
            return
        self.current_mask_idx = (self.current_mask_idx + 1) % len(self.masks)
        self.status_var.set(
            f"当前掩码: {self.current_mask_idx + 1}/{len(self.masks)}, 分数: {self.scores[self.current_mask_idx]:.3f}")
        if self.image_np is not None: self.display_image(self.image_np)

    def select_mask(self):
        if self.masks is None or len(self.masks) == 0 or self.current_mask_idx >= len(self.masks):
            messagebox.showwarning("警告", "没有可选择的掩码")
            return
        self.save_to_history()
        self.selected_mask = self.masks[self.current_mask_idx].copy()
        self.is_modified = True
        messagebox.showinfo("提示", f"已选择掩码 {self.current_mask_idx + 1}/{len(self.masks)}，请分配标签")
        if self.image_np is not None: self.display_image(self.image_np)

    def on_label_change(self, event=None):
        new_label = self.label_var.get()
        if new_label and new_label not in self.available_labels:
            self.available_labels.append(new_label)
            self.label_combo['values'] = self.available_labels
            if len(self.available_labels) > len(self.colors):
                self.colors = self.generate_colors(len(self.available_labels))
        self.current_label = new_label

    def confirm_label(self):
        if self.selected_mask is None:
            messagebox.showwarning("警告", "请先选择一个掩码 (通过SAM预测或多边形绘制)")
            return
        label = self.current_label
        if not label or label == "" or label == DEFAULT_LABELS[0]:
            messagebox.showwarning("警告", "请选择一个有效的标签 (非背景)")
            return

        self.save_to_history()

        if label not in self.annotation_masks:
            self.annotation_masks[label] = []
        self.annotation_masks[label].append(self.selected_mask.copy())
        action = "添加" if len(self.annotation_masks[label]) == 1 else "叠加"

        self.is_modified = True
        self.selected_mask = None

        self.points = []
        self.labels = []
        self.masks = None
        self.scores = None
        self.current_mask_idx = 0
        self.clear_polygon()

        messagebox.showinfo("提示", f"已{action}并锁定标签为 '{label}' 的区域")

        self.label_var.set(DEFAULT_LABELS[0])
        self.current_label = DEFAULT_LABELS[0]

        if self.image_np is not None: self.display_image(self.image_np)

    def _prepare_for_editing(self):
        """为编辑模式准备数据，计算每个mask的边界框"""
        self.editable_regions = []
        if self.image_np is None:
            return

        for label, masks_list in self.annotation_masks.items():
            for mask in masks_list:
                contours, _ = cv2.findContours(mask.astype(np.uint8), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
                if not contours:
                    continue
                all_points = np.concatenate(contours)
                x, y, w, h = cv2.boundingRect(all_points)
                self.editable_regions.append({'mask': mask, 'label': label, 'bbox': (x, y, w, h)})

    def _clear_selection_state(self):
        """清除编辑模式下的所有选择和悬停状态"""
        self.selected_region_index = None
        self.hovered_region_index = None
        self.update_label_button.config(state=tk.DISABLED)
        self.label_var.set(DEFAULT_LABELS[0])
        self.current_label = DEFAULT_LABELS[0]
        self.editable_regions = []

    def update_selected_label(self):
        """更新当前选中区域的标签"""
        if self.selected_region_index is None:
            messagebox.showwarning("警告", "没有选中的区域可更新。")
            return

        new_label = self.label_var.get()
        if not new_label or new_label == DEFAULT_LABELS[0]:
            messagebox.showwarning("警告", "请选择一个有效的新标签。")
            return

        region_to_update = self.editable_regions[self.selected_region_index]
        old_label = region_to_update['label']
        mask_to_move = region_to_update['mask']

        if new_label == old_label:
            messagebox.showinfo("提示", "新旧标签相同，未做更改。")
            return

        self.save_to_history()

        self.annotation_masks[old_label] = [m for m in self.annotation_masks[old_label] if m is not mask_to_move]
        if not self.annotation_masks[old_label]:
            del self.annotation_masks[old_label]

        if new_label not in self.annotation_masks:
            self.annotation_masks[new_label] = []
        self.annotation_masks[new_label].append(mask_to_move)

        self.is_modified = True
        messagebox.showinfo("成功", f"区域标签已从 '{old_label}' 更新为 '{new_label}'。")

        self._clear_selection_state()
        self._prepare_for_editing()
        self.display_image(self.image_np)

    def complete_annotation(self):
        if not self.annotation_masks:
            messagebox.showwarning("警告", "没有任何标注，无法完成")
            return
        if self.image_name == "" or self.image_np is None:
            messagebox.showerror("错误", "没有加载图像，无法保存。")
            return

        try:
            base_name = self.image_name.rsplit('.', 1)[0]
            json_file = os.path.join(self.jsons_path, base_name + '.json')

            jpg_file_name = base_name + '.jpg'
            jpg_file_path = os.path.join(self.jpgs_path, jpg_file_name)

            img_pil = Image.fromarray(self.image_np)
            img_pil.save(jpg_file_path, "JPEG")

            height, width = self.image_np.shape[:2]
            data = {
                "version": "5.0.1",
                "flags": {},
                "shapes": [],
                "imagePath": jpg_file_name,
                "imageData": None,
                "imageHeight": height,
                "imageWidth": width
            }

            for label, masks_list in self.annotation_masks.items():
                for mask_item in masks_list:
                    if not np.any(mask_item):
                        continue
                    contours, _ = cv2.findContours(
                        mask_item.astype(np.uint8),
                        cv2.RETR_EXTERNAL,
                        cv2.CHAIN_APPROX_SIMPLE
                    )
                    for contour in contours:
                        if contour.shape[0] < 3:
                            continue
                        points = contour.reshape(-1, 2).tolist()
                        shape = {
                            "label": label,
                            "points": points,
                            "group_id": None,
                            "shape_type": "polygon",
                            "flags": {}
                        }
                        data["shapes"].append(shape)

            if not data["shapes"]:
                messagebox.showwarning("警告", "没有有效的标注形状可以保存。")
                return

            with open(json_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)

            self.previous_annotations[self.image_name] = self.annotation_masks.copy()
            self.is_modified = False
            self.annotation_complete = True
            messagebox.showinfo("提示", f"标注已保存到 {json_file}\n图像副本已保存到 {jpg_file_path}")

            self._save_last_session_info()
            self.next_image()

        except Exception as e:
            print(f"保存标注失败: {e}")
            traceback.print_exc()
            messagebox.showerror("错误", f"保存标注失败: {str(e)}")


# -----------------------------------------------------------------------------------------
# 注意：此文件不包含 main() 函数或 if __name__ == "__main__":
# 因为它现在是一个模块，其类 `InteractiveSAM2Annotator` 将由 `main.py` 导入并启动。
# -----------------------------------------------------------------------------------------