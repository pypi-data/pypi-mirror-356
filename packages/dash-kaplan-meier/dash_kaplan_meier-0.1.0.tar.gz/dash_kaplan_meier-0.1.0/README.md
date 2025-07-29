# DashKaplanMeier Dash Component

Dash component built with React to render **Kaplan–Meier survival curves** with enhanced interactivity and styling options. This component is ideal for visualizing survival analysis data directly within Dash applications.

## Features

- Plot Kaplan–Meier survival curves from preprocessed data.
- Support for multiple curves with different group labels.
- Interactive tooltips and hover effects.
- Customizable colors and dimensions.
- Fully integrated with Dash callback system.

## Installation

```bash
pip install dash-kaplan-meier
````

## Install requirements

```bash
pip install dash
pip install lifelines
```

## Usage

Here’s how to use the `DashKaplanMeier` component in your Dash app:

```python
import dash
from dash import html, Dash
import dash_kaplan_meier as dkm
from dash_kaplan_meier.survival_stats import compute_survival_stats

# Example data
time        = [your time values list here]
event       = [your event values list here]
group       = [you rgroup values list here]

# Compute statistics
stats       = compute_survival_stats(time ,event, group)

# Dash app
app         = Dash()

# Dash app layout with DashKaplanMeier component
app.layout = html.Div([
    dkm.DashKaplanMeier(
        id              = 'km-example',
        time            = time,
        event           = event,
        group           = group,
        showCIs         = True,
        colors          = ['blue', 'green', 'red'],
        showStatistics  = True,
        logrankP        = stats["logrank_p"],
        coxP            = stats["cox_p"],
        hazardRatio     = stats["hazard_ratio"],
        layout          ={  'title': 'Kaplan-Meier Survival Curve Example',
                            "xaxis": {"title": {"text": "Time (months)"}},
                            "yaxis": {"title": {"text": "Survival Probability"}}},
        title           = "Kaplan-Meier curves",
        config          = {'responsive': True}
    )
])

if __name__ == '__main__':
    app.run(debug=True)

```

## Plot Example

![Survival Example](https://github.com/XLlobet/dash-kaplan-meier/blob/main/survival.png?raw=true)

## Contributing

See [CONTRIBUTING.md](https://github.com/XLlobet/dash-kaplan-meier/blob/main/dash_kaplan_meier/CONTRIBUTING.md)

## License

MIT License. See `LICENSE` file for details.