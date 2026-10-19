import argparse
import csv
from pathlib import Path


CLASS_COLUMNS = {
    "Core": "average_core_nullomers",
    "Softcore": "average_softcore_nullomers",
    "Shell": "average_shell_nullomers",
    "Cloud": "average_cloud_nullomers",
}

CLASS_COLOURS = {
    "Core": "#1f77b4",
    "Softcore": "#ff7f0e",
    "Shell": "#2ca02c",
    "Cloud": "#d62728",
}


def read_average_stats(input_file):
    rows = []

    with open(input_file, newline="") as csvfile:
        reader = csv.DictReader(csvfile)

        required_columns = ["sample_size", *CLASS_COLUMNS.values()]
        missing_columns = [
            column for column in required_columns
            if column not in reader.fieldnames
        ]

        if missing_columns:
            raise ValueError(
                "Input CSV is missing required columns: "
                + ", ".join(missing_columns)
            )

        for row in reader:
            rows.append({
                "sample_size": int(row["sample_size"]),
                "Core": float(row["average_core_nullomers"]),
                "Softcore": float(row["average_softcore_nullomers"]),
                "Shell": float(row["average_shell_nullomers"]),
                "Cloud": float(row["average_cloud_nullomers"]),
            })

    rows.sort(key=lambda item: item["sample_size"])

    if not rows:
        raise ValueError("Input CSV contains no data rows.")

    return rows


def scale_value(value, input_min, input_max, output_min, output_max):
    if input_max == input_min:
        return (output_min + output_max) / 2

    return output_min + (
        (value - input_min) / (input_max - input_min)
    ) * (output_max - output_min)


def make_polyline_points(rows, class_name, x_min, x_max, y_min, y_max, plot_left, plot_right, plot_top, plot_bottom):
    points = []

    for row in rows:
        x = scale_value(
            row["sample_size"],
            x_min,
            x_max,
            plot_left,
            plot_right,
        )

        y = scale_value(
            row[class_name],
            y_min,
            y_max,
            plot_bottom,
            plot_top,
        )

        points.append(f"{x:.2f},{y:.2f}")

    return " ".join(points)


def make_svg(rows, title):
    width = 1200
    height = 800

    margin_left = 110
    margin_right = 230
    margin_top = 90
    margin_bottom = 100

    plot_left = margin_left
    plot_right = width - margin_right
    plot_top = margin_top
    plot_bottom = height - margin_bottom

    x_values = [row["sample_size"] for row in rows]
    y_values = []

    for row in rows:
        for class_name in CLASS_COLUMNS:
            y_values.append(row[class_name])

    x_min = min(x_values)
    x_max = max(x_values)
    y_min = 0
    y_max = max(y_values)

    if y_max == 0:
        y_max = 1

    y_max = y_max * 1.05

    svg = []

    svg.append(f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">')
    svg.append('<rect width="100%" height="100%" fill="white"/>')

    svg.append(f'<text x="{width / 2}" y="45" text-anchor="middle" font-family="Arial" font-size="28" font-weight="bold">{title}</text>')

    svg.append(f'<line x1="{plot_left}" y1="{plot_bottom}" x2="{plot_right}" y2="{plot_bottom}" stroke="black" stroke-width="2"/>')
    svg.append(f'<line x1="{plot_left}" y1="{plot_top}" x2="{plot_left}" y2="{plot_bottom}" stroke="black" stroke-width="2"/>')

    y_tick_count = 6
    for tick in range(y_tick_count + 1):
        value = y_min + ((y_max - y_min) / y_tick_count) * tick
        y = scale_value(value, y_min, y_max, plot_bottom, plot_top)

        svg.append(f'<line x1="{plot_left - 6}" y1="{y:.2f}" x2="{plot_left}" y2="{y:.2f}" stroke="black" stroke-width="1"/>')
        svg.append(f'<line x1="{plot_left}" y1="{y:.2f}" x2="{plot_right}" y2="{y:.2f}" stroke="#dddddd" stroke-width="1"/>')
        svg.append(f'<text x="{plot_left - 12}" y="{y + 5:.2f}" text-anchor="end" font-family="Arial" font-size="14">{value:.0f}</text>')

    x_tick_values = list(range(x_min, x_max + 1, 5))

    if x_min not in x_tick_values:
        x_tick_values.insert(0, x_min)

    if x_max not in x_tick_values:
        x_tick_values.append(x_max)

    for value in x_tick_values:
        x = scale_value(value, x_min, x_max, plot_left, plot_right)

        svg.append(f'<line x1="{x:.2f}" y1="{plot_bottom}" x2="{x:.2f}" y2="{plot_bottom + 6}" stroke="black" stroke-width="1"/>')
        svg.append(f'<text x="{x:.2f}" y="{plot_bottom + 28}" text-anchor="middle" font-family="Arial" font-size="14">{value}</text>')

    for class_name in CLASS_COLUMNS:
        points = make_polyline_points(
            rows,
            class_name,
            x_min,
            x_max,
            y_min,
            y_max,
            plot_left,
            plot_right,
            plot_top,
            plot_bottom,
        )

        colour = CLASS_COLOURS[class_name]

        svg.append(
            f'<polyline points="{points}" fill="none" stroke="{colour}" stroke-width="3" stroke-linejoin="round" stroke-linecap="round"/>'
        )

        for row in rows:
            x = scale_value(row["sample_size"], x_min, x_max, plot_left, plot_right)
            y = scale_value(row[class_name], y_min, y_max, plot_bottom, plot_top)

            svg.append(f'<circle cx="{x:.2f}" cy="{y:.2f}" r="3.5" fill="{colour}"/>')

    svg.append(f'<text x="{(plot_left + plot_right) / 2}" y="{height - 35}" text-anchor="middle" font-family="Arial" font-size="18">Number of Genomes Used</text>')

    svg.append(
        f'<text x="30" y="{(plot_top + plot_bottom) / 2}" text-anchor="middle" font-family="Arial" font-size="18" transform="rotate(-90, 30, {(plot_top + plot_bottom) / 2})">Average Nullomer Count</text>'
    )

    legend_x = plot_right + 45
    legend_y = plot_top + 25

    svg.append(f'<text x="{legend_x}" y="{legend_y - 20}" font-family="Arial" font-size="18" font-weight="bold">Class</text>')

    for index, class_name in enumerate(CLASS_COLUMNS):
        y = legend_y + index * 35
        colour = CLASS_COLOURS[class_name]

        svg.append(f'<line x1="{legend_x}" y1="{y}" x2="{legend_x + 35}" y2="{y}" stroke="{colour}" stroke-width="4"/>')
        svg.append(f'<circle cx="{legend_x + 17.5}" cy="{y}" r="4" fill="{colour}"/>')
        svg.append(f'<text x="{legend_x + 50}" y="{y + 5}" font-family="Arial" font-size="16">{class_name}</text>')

    svg.append("</svg>")

    return "\n".join(svg)


def write_svg(output_file, svg_content):
    output_path = Path(output_file)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(svg_content)


def main():
    parser = argparse.ArgumentParser(
        description="Create a line chart from average random pan-genome nullomer statistics."
    )

    parser.add_argument(
        "input_csv",
        help="Path to average_random_pan_stats.csv",
    )

    parser.add_argument(
        "-o",
        "--output",
        default="average_nullomer_class_chart.svg",
        help="Output SVG file path. Default: average_nullomer_class_chart.svg",
    )

    parser.add_argument(
        "--title",
        default="Average Nullomer Classes Across Random Genome Samples",
        help="Chart title.",
    )

    args = parser.parse_args()

    rows = read_average_stats(args.input_csv)
    svg_content = make_svg(rows, args.title)
    write_svg(args.output, svg_content)

    print(f"Chart written to: {args.output}")


if __name__ == "__main__":
    main()