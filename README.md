# Starbucks Recommendation Engine & Product Optimizer

A data science project building two algorithms for Starbucks:
1. **New Frappuccino Design Optimizer** — finds optimal nutrition/pricing attributes for new product launches
2. **Personalized Recommendation Engine** — content-based drink + customization recommendations per customer persona

## Notebooks (8)

| # | Notebook | Description |
|---|----------|-------------|
| 1 | [Menu EDA](https://www.kaggle.com/code/shiratoriseto/starbucks-menu-eda-nutrition-pricing-analysis) | Category distribution, price/calorie analysis |
| 2 | [Macro Elasticity](https://www.kaggle.com/code/shiratoriseto/starbucks-macro-elasticity-cpi-wage-analysis) | CPI trends, wage analysis, price sensitivity |
| 3 | [Synthetic Data](https://www.kaggle.com/code/shiratoriseto/starbucks-synthetic-purchase-data-generation) | 100K transaction generation with real constraints |
| 4 | [Product Optimizer](https://www.kaggle.com/code/shiratoriseto/starbucks-new-frappuccino-design-optimizer) | New Frappuccino design optimization |
| 5 | [Recommendation Engine](https://www.kaggle.com/code/shiratoriseto/starbucks-personalized-recommendation-engine) | Personalized drink + customization recommendations |
| 6 | [Validation](https://www.kaggle.com/code/shiratoriseto/starbucks-validation-stress-test) | Benchmark comparison, perturbation tests, stability |
| 7 | [April Frappuccino](https://www.kaggle.com/code/shiratoriseto/starbucks-april-2026-frappuccino-launch) | April 2026 optimal new product specification |
| 8 | [April Persona Sim](https://www.kaggle.com/code/shiratoriseto/starbucks-april-persona-recommendation-simulation) | Persona-based recommendation simulation |

## Kaggle Resources

- **Dataset:** [Starbucks Recommendation Engine Data](https://www.kaggle.com/datasets/shiratoriseto/starbucks-recommendation-engine) (Usability 10.0)
- **Model 1:** [Recommendation Engine](https://www.kaggle.com/models/shiratoriseto/starbucks-recommendation-engine-model) (Usability 10.0)
- **Model 2:** [Frappuccino Optimizer](https://www.kaggle.com/models/shiratoriseto/starbucks-frappuccino-optimizer) (Usability 10.0)

## Data Sources

| Source | License | Used for |
|--------|---------|----------|
| Starbucks published nutrition data | Public | Menu items, calories, caffeine |
| [FRED](https://fred.stlouisfed.org/) | Public domain | CPI, average hourly earnings |
| [Open-Meteo](https://open-meteo.com/) | CC-BY 4.0 | Daily temperature, 5 US cities |
| Synthetic (this project) | ODbL 1.0 | 100K purchase transactions |

## Synthetic Data Approach

Transaction data is synthetic — generated from probability distributions constrained by real-world data. Every assumption is documented in Notebook 3 and validated in Notebook 6. The framework (not the specific numbers) is the deliverable.

## Related Project

- [Manhattan Cafe Wars: Starbucks Spatial Analysis](https://github.com/seto-siratori/starbucks-kaggle) — 15-notebook spatial data science series
