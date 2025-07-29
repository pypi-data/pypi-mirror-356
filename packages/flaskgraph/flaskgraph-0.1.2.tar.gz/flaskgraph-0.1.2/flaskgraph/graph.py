import json
import uuid
from markupsafe import Markup

class ChartJS:
    COLOR_THEMES = {
        "blue": {"background": "rgba(59, 130, 246, 0.8)", "border": "rgba(59, 130, 246, 1)"},
        "green": {"background": "rgba(34, 197, 94, 0.8)", "border": "rgba(34, 197, 94, 1)"},
        "red": {"background": "rgba(239, 68, 68, 0.8)", "border": "rgba(239, 68, 68, 1)"},
        "yellow": {"background": "rgba(250, 204, 21, 0.8)", "border": "rgba(250, 204, 21, 1)"},
        "orange": {"background": "rgba(251, 146, 60, 0.8)", "border": "rgba(251, 146, 60, 1)"},
        "purple": {"background": "rgba(168, 85, 247, 0.8)", "border": "rgba(168, 85, 247, 1)"},
        "pink": {"background": "rgba(244, 114, 182, 0.8)", "border": "rgba(244, 114, 182, 1)"},
        "teal": {"background": "rgba(45, 212, 191, 0.8)", "border": "rgba(45, 212, 191, 1)"},
        "sky": {"background": "rgba(56, 189, 248, 0.8)", "border": "rgba(56, 189, 248, 1)"},
        "lime": {"background": "rgba(132, 204, 22, 0.8)", "border": "rgba(132, 204, 22, 1)"},
        "slate": {"background": "rgba(100, 116, 139, 0.8)", "border": "rgba(100, 116, 139, 1)"},
        "gray": {"background": "rgba(156, 163, 175, 0.8)", "border": "rgba(156, 163, 175, 1)"},
        "zinc": {"background": "rgba(113, 113, 122, 0.8)", "border": "rgba(113, 113, 122, 1)"},
        "neon-green": {"background": "rgba(22, 255, 107, 0.8)", "border": "rgba(22, 255, 107, 1)"},
        "neon-pink": {"background": "rgba(255, 20, 147, 0.8)", "border": "rgba(255, 20, 147, 1)"},
        "neon-blue": {"background": "rgba(0, 245, 255, 0.8)", "border": "rgba(0, 245, 255, 1)"}
    }

    def _gen_id(self):
        return uuid.uuid4().hex[:8]

    def _render(self, chart_id, chart_type, labels, data_dict, label_color, legend, grid, colortheme):
        dataset_name, dataset_values = list(data_dict.items())[0]
        colors = self.COLOR_THEMES.get(colortheme, self.COLOR_THEMES["blue"])
        label_colors = {"standard": "#999999", "dark": "#252525", "light": "#f0f0f0"}
        label_color_val = label_colors.get(label_color, "#252525")
        grid_config = str(grid).lower()

        js = f"""
<canvas id="{chart_id}"></canvas>
<script>
const labels_{chart_id} = {json.dumps(labels)};
const ctx_{chart_id} = document.getElementById('{chart_id}').getContext('2d');

new Chart(ctx_{chart_id}, {{
  type: '{chart_type}',
  data: {{
    labels: labels_{chart_id},
    datasets: [{{
      label: '{dataset_name}',
      data: {json.dumps(dataset_values)},
      backgroundColor: '{colors["background"]}',
      borderColor: '{colors["border"]}',
      tension: 0.4
    }}]
  }},
  options: {{
    responsive: true,
    maintainAspectRatio: false,
    plugins: {{
      legend: {{
        display: {str(legend).lower()},
        labels: {{ color: '{label_color_val}' }}
      }}
    }},
    scales: {{
      y: {{
        beginAtZero: true,
        ticks: {{ color: '{label_color_val}' }},
        grid: {{
          display: {grid_config},
          drawBorder: {grid_config}
        }}
      }},
      x: {{
        ticks: {{ color: '{label_color_val}' }},
        grid: {{
          display: {grid_config},
          drawBorder: {grid_config}
        }}
      }}
    }}
  }}
}});
</script>
"""
        return Markup(js)

    def bar(self, labels, data, label_color="dark", legend=True, grid=True, colortheme="blue"):
        return self._render(f"chart_{self._gen_id()}", "bar", labels, data, label_color, legend, grid, colortheme)

    def line(self, labels, data, label_color="dark", legend=True, grid=True, colortheme="blue"):
        return self._render(f"chart_{self._gen_id()}", "line", labels, data, label_color, legend, grid, colortheme)

    def donut(self, labels, data, label_color="dark", legend=True, grid=True, colortheme="blue"):
        return self._render(f"chart_{self._gen_id()}", "doughnut", labels, data, label_color, legend, grid, colortheme)

    def scatter(self, labels, data, label_color="dark", legend=True, grid=True, colortheme="blue"):
        return self._render(f"chart_{self._gen_id()}", "scatter", labels, data, label_color, legend, grid, colortheme)


graph = ChartJS()
