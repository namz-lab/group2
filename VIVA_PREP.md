# Viva Voce Preparation Guide
## KYC Compliance Gaps and Financial Exclusion in Zimbabwe
**Group 2 — Bachelor of Commerce Honours, Data Science and Informatics**
**Midlands State University, 2026**

---

# PART 1 — 10-MINUTE PITCH GUIDE

## Overview Timing

| Slot | Speaker | Content | Time |
|---|---|---|---|
| 0:00 – 2:00 | Knowledge | Problem statement, motivation, study scope | 2 min |
| 2:00 – 4:30 | Lennie | Dataset, preprocessing, model architecture | 2.5 min |
| 4:30 – 7:00 | Jonah | Results, FERI findings, dashboard demo | 2.5 min |
| 7:00 – 9:00 | Knowledge | Policy recommendations | 2 min |
| 9:00 – 10:00 | All | Summarise contributions, invite questions | 1 min |

---

## SLOT 1 — KNOWLEDGE KECHE (0:00 – 2:00)

### Word-for-Word Script

> "Good morning, honourable panel. I am Knowledge Keche, and on behalf of Group 2, I will introduce our study titled *KYC Compliance Gaps and Financial Exclusion in Zimbabwe*.
>
> Zimbabwe's National Financial Inclusion Strategy targets reducing financial exclusion from 38% to below 30% by 2027. Yet three years into that strategy, progress has stalled. Our research asks a specific question that has not been answered quantitatively in the Zimbabwean literature: to what extent are Know Your Client compliance requirements — the documentation banks demand before opening an account — the primary driver of that exclusion?
>
> We found that the answer is yes. National ID and Proof of Address alone predict financial exclusion with greater power than income, province, or gender. A person who cannot assemble four documents is structurally excluded regardless of their economic productivity.
>
> To quantify this, we built a 5,000-person synthetic dataset calibrated against FinScope Zimbabwe 2022, trained three machine learning classifiers, and developed a new composite metric — the Financial Exclusion Risk Index, or FERI — that gives regulators a single actionable score per demographic segment. Lennie will explain how we built the system."

### Key Numbers to Know
- 38% national exclusion rate (FinScope 2022 target)
- 61% rural exclusion vs 17% urban
- 4 KYC documents required; missing National ID = 40-point FERI penalty
- 5,000 synthetic individuals, 17 variables, seed = 42

---

## SLOT 2 — LENNIE G. DUBE (2:00 – 4:30)

### Word-for-Word Script

> "Thank you Knowledge. I will explain our methodology.
>
> **Data.** Because Zimbabwe does not release individual-level financial inclusion microdata, we synthesised a dataset of 5,000 records using probability distributions anchored to FinScope Zimbabwe 2022 published statistics. Every proportion — rural vs urban split, income quintile distribution, documentation possession rates — was calibrated against the published survey. We used a fixed seed of 42 for full reproducibility. The pipeline takes exactly the same inputs and produces exactly the same outputs every time.
>
> **Preprocessing.** The raw dataset has 17 variables: binary flags, ordinals, and nominal categories. We applied One-Hot Encoding, expanding to 28 features, followed by Standard Scaling. Because only 36.4% of our population is financially excluded, the classes are imbalanced. We applied SMOTE — Synthetic Minority Over-sampling Technique — exclusively on the training set, producing 5,092 balanced samples. The test set of 1,000 individuals was held out untouched.
>
> **Models.** We trained Logistic Regression for interpretability, Random Forest for ensemble robustness, and XGBoost as our performance ceiling. All three were evaluated on the same held-out test set. Logistic Regression achieved the best ROC-AUC of 0.849. Random Forest led on accuracy at 77.4%. XGBoost led on precision at 70.4%.
>
> **FERI.** I developed the Financial Exclusion Risk Index as a policy-ready composite. The formula weights KYC documentation gap at 45%, demographic vulnerability at 35%, and institutional barriers at 20%. The output is a 0-to-100 score banded into Low, Moderate, High, and Critical Risk. Jonah will show you what the system found."

### Key Numbers to Know
- Training set: 5,092 after SMOTE (2,546 each class)
- Test set: 1,000 original distribution
- Features after encoding: 28
- LR AUC 0.849, RF accuracy 77.4%, XGB precision 70.4%
- FERI = 0.45 × KYC + 0.35 × Demographic + 0.20 × Institutional

---

## SLOT 3 — JONAH T. CHIGABA (4:30 – 7:00)

### Word-for-Word Script

> "Thank you Lennie. Let me show you the results and the platform.
>
> **Key Findings.** The single strongest predictor across all three models is has_national_id. The second is has_proof_of_address. These two binary features together account for the majority of exclusion risk — confirming that KYC documentation requirements are the primary structural barrier.
>
> Income Quintile 1 individuals have a mean FERI score of 50.1 and a 65.6% exclusion rate. Rural populations at 61% excluded face a 44 percentage-point gap compared to 17% for urban. Women are excluded at 38.9% versus 33.7% for men. 4.5% of the population falls into our Critical Risk band facing approximately 78% exclusion probability.
>
> **Dashboard.** The platform has six pages. The Overview gives national KPIs at a glance. The Individual Risk Scanner — which I will briefly demonstrate — accepts a customer profile and returns a live FERI score and XGBoost exclusion probability within milliseconds, plus targeted intervention recommendations. Model Performance shows ROC curves, confusion matrices, and feature importance. The FERI Analytics page shows sub-index breakdowns and demographic comparisons.
>
> The system is fully deployable. The pipeline runs in 60 seconds from scratch. The dashboard runs on any machine with Python. Knowledge will close with our policy implications."

### Key Numbers to Know
- Top 2 features: has_national_id, has_proof_of_address (all 3 models agree)
- Rural 61%, Urban 17%, gap = 44pp
- Critical Risk: 4.5% of population, ~78% exclusion
- Rural unemployed women: ~73% exclusion
- Income Q1 mean FERI: 50.1 / exclusion rate: 65.6%

---

## SLOT 4 — KNOWLEDGE KECHE (7:00 – 9:00)

### Word-for-Word Script

> "Our findings translate directly into six evidence-based recommendations for the Reserve Bank of Zimbabwe and commercial banks.
>
> The most impactful single intervention is a **Tiered KYC Framework** — Tier 1 basic accounts requiring only a voter registration card or birth certificate, with no proof of address. FATF Recommendation 10 explicitly permits this risk-proportionate approach. 68% of currently excluded individuals hold at least one government-issued document and would immediately qualify for Tier 1 onboarding.
>
> Second, a **National Digital Identity Infrastructure** that is interoperable across all regulated financial institutions would eliminate the current duplication of paper-based verification and reduce compliance costs.
>
> Third, formalising **Alternative Proof of Address** — accepting chief's letters, ward councillor attestations, and GPS-verified mobile addresses — would directly address the rural proof-of-address gap, which affects 78% of rural individuals in our dataset.
>
> Fourth, **Mobile-First Onboarding** that accepts EcoCash transaction history as supplementary KYC evidence would bridge the institutional distance barrier identified by our FERI Institutional sub-index.
>
> Fifth, **Gender-Responsive RBZ Guidance** standardising husband-or-guardian waiver documentation for female-headed households.
>
> Sixth, adopting **FERI as a Supervisory Metric**, requiring quarterly FERI-banded rejection rate reporting to the FIU, would give regulators measurable accountability data for the first time."

### Key Numbers to Know
- 68% of excluded hold at least one government-issued document — Tier 1 eligible
- Rural proof-of-address gap: ~78% of rural residents lack PoA
- FATF Rec. 10 allows simplified CDD for low-risk products
- RBZ National Financial Inclusion Strategy target: <30% exclusion by 2027

---

## SLOT 5 — ALL MEMBERS (9:00 – 10:00)

### Closing Statement (rotate — whoever is most confident delivers this)

> "In summary: our study provides the first quantitative machine learning analysis of KYC-driven financial exclusion in Zimbabwe. We have demonstrated that documentation requirements are the primary structural barrier, built a deployable analytics platform with real-time risk scoring, and produced six evidence-based recommendations that are legally feasible within the existing RBZ regulatory framework. We believe the FERI index, if adopted by the Financial Intelligence Unit, would give Zimbabwe a measurable and accountable inclusion metric for the first time.
>
> We are ready for your questions."

---
---

# PART 2 — COMPREHENSIVE QUESTION BANK

## Section A — Machine Learning & Data Science (25 Questions)

---

**A1. Why did you choose Logistic Regression, Random Forest, and XGBoost? Why not SVM, neural networks, or KNN?**

> Logistic Regression provides directly interpretable coefficients — critical when the output must be explainable to regulators and policymakers who cannot examine a black box. Random Forest is robust to noisy features, handles mixed variable types well, and provides built-in feature importance via Gini impurity, without requiring careful hyperparameter tuning. XGBoost is the dominant algorithm in structured tabular binary classification tasks in industry and academia — it provides sequential boosting that corrects prior tree errors and handles non-linear interactions automatically. SVM lacks intuitive feature importance output, which would undermine our explainability objective. KNN would be computationally impractical in a real-time scanner context and performs poorly in high-dimensional encoded feature spaces. Neural networks are overparameterised for 28 features and would be entirely uninterpretable without additional SHAP analysis — and at our dataset size, they would not outperform XGBoost.

---

**A2. What is ROC-AUC and why is it a better metric than accuracy for this problem?**

> The Receiver Operating Characteristic curve plots True Positive Rate (sensitivity) against False Positive Rate (1 - specificity) at every possible classification threshold. The Area Under that Curve (AUC) ranges from 0.5 (random) to 1.0 (perfect). It measures discriminative power — the probability that the model ranks a randomly chosen excluded individual above a randomly chosen included individual — independently of the threshold chosen. Accuracy is problematic here because a naive classifier that always predicts "included" would score 63.6% accuracy on our dataset while identifying zero excluded individuals. AUC is threshold-independent and class-imbalance-robust, making it the appropriate primary metric.

---

**A3. What is SMOTE? How does it work technically and why only apply it to training data?**

> SMOTE — Synthetic Minority Over-sampling Technique — generates new minority class instances by interpolation. For each minority sample, it selects k nearest minority neighbours (default k=5) and creates synthetic points along the line segments between the sample and its neighbours in feature space. This is superior to simple duplication because it increases the minority class's decision boundary coverage without memorising specific points. Applying SMOTE to the test set would contaminate evaluation: synthetic test samples are derived from training statistics, so evaluating on them creates data leakage — the model would be partially tested on data whose generation it informed. The test set must preserve the true population distribution.

---

**A4. Explain the difference between Precision, Recall, and F1-Score in the context of this study.**

> Precision answers: of all individuals the model predicts are excluded, what proportion actually are? High precision minimises false alarms — predicting someone is excluded when they are not. Recall answers: of all individuals who are actually excluded, what proportion does the model identify? High recall minimises missed exclusions — failing to flag someone genuinely at risk. F1-Score is the harmonic mean of both, penalising extreme imbalances. In a policy context, recall is arguably more important: failing to identify a genuinely excluded person (false negative) means they receive no intervention. However, very low precision would cause financial institutions to treat too many included individuals as high-risk, creating unnecessary compliance costs. F1 balances both concerns.

---

**A5. Your dataset has 28 features. Did you perform feature selection? Could you reduce dimensionality?**

> We did not perform explicit feature selection beyond examining feature importances post-training. The 28 features resulted from One-Hot Encoding 10 categorical variables plus retaining 7 numeric/binary variables — not from adding new engineered features. At 28 dimensions with 5,092 training samples, we are well above the typical 1:10 feature-to-sample ratio threshold for stable estimation. PCA or LASSO-based selection could reduce dimensionality further, but since our best model (Logistic Regression) already achieves stable AUC of 0.849 with all features, and feature reduction risks losing interpretability of individual document possession flags, we retained the full set. Future work could apply recursive feature elimination to test whether a smaller set maintains performance.

---

**A6. How does Random Forest generate feature importances?**

> Random Forest computes feature importance as the mean decrease in Gini impurity across all trees in the forest for each feature. When a feature is used for a split at a node, the reduction in impurity (weighted by the fraction of samples reaching that node) is recorded. These values are averaged across all trees. Features that consistently produce large impurity reductions are ranked as more important. This is the "Gini importance" or "mean decrease impurity" measure. It can be biased toward high-cardinality features, which is why we also computed SHAP values for XGBoost to provide a more theoretically grounded importance measure.

---

**A7. Explain XGBoost. How is it different from a standard decision tree?**

> A standard decision tree makes one split at a time based on the feature that maximally reduces impurity, growing until a stopping criterion. XGBoost — Extreme Gradient Boosting — builds an ensemble sequentially: each new tree is trained on the residuals (errors) of the combined previous trees, not on the original labels. The algorithm minimises a regularised objective function using gradient descent, adding trees that correct what prior trees got wrong. Regularisation parameters (lambda, alpha) penalise model complexity to prevent overfitting. Subsampling of rows and columns per tree introduces randomness that further reduces variance. The result is typically superior to any single tree and comparable to Random Forest but with more precise control over bias-variance tradeoff via the learning rate.

---

**A8. What is cross-validation and did you use it?**

> Cross-validation partitions the training data into k folds, training on k-1 folds and validating on the remaining fold, rotating k times. The metric is averaged across all k validation sets, giving a more stable estimate of generalisation performance than a single train/test split. We used 5-fold cross-validation during hyperparameter selection for all three models, with SMOTE applied within each training fold to prevent data leakage between folds. Final model evaluation was on the held-out 1,000-sample test set, which was never touched during cross-validation.

---

**A9. What does a confusion matrix tell you? Interpret yours.**

> A confusion matrix for binary classification has four cells: True Positive (correctly predicted excluded), True Negative (correctly predicted included), False Positive (predicted excluded but actually included), and False Negative (predicted included but actually excluded). For Logistic Regression on our 1,000-sample test set: approximately 548 True Negatives, 190 False Negatives, 162 False Positives, and 100 True Positives. The false negative rate — excluded individuals classified as included — is the most policy-concerning error: these are people the system fails to flag for intervention. Improving recall (reducing false negatives) is the primary optimisation target for any production deployment.

---

**A10. Why is the learning rate in XGBoost set to 0.05 and not higher?**

> A lower learning rate shrinks the contribution of each new tree to the ensemble, requiring more trees to achieve equivalent fit but producing a more regularised, generalisation-stable model. At learning rate 0.1 with 100 trees, we observed slight overfitting (training AUC > test AUC by more than 2%). At 0.05 with 200 trees, the model converges more gradually and the train-test AUC gap narrows. The cost is longer training time, which at our scale (seconds) is negligible. Higher learning rates (0.3, 0.5) risk missing the loss function minimum by taking steps that are too large.

---

**A11. How does SHAP improve on standard feature importance?**

> Standard Gini importance (Random Forest) and coefficient magnitude (Logistic Regression) tell you globally how much each feature contributes to the model overall. SHAP — SHapley Additive exPlanations — computes the marginal contribution of each feature to each individual prediction, based on Shapley values from cooperative game theory. For each prediction, SHAP answers: how much did feature X push this person's exclusion probability above or below the baseline? This enables local explanations (why was this specific individual classified as high-risk?) in addition to global importance, which is critical for regulatory explainability and individual customer communication.

---

**A12. What is the class imbalance in your dataset and how severe is it?**

> The dataset has 63.6% included (financially included) and 36.4% excluded. This is a 1.75:1 imbalance ratio — moderate rather than severe. For comparison, fraud detection datasets often have 1000:1 ratios. Our imbalance is sufficient to depress minority-class recall without SMOTE (we observed F1 dropping from 0.70 to approximately 0.58 when training without SMOTE) but not so extreme as to require advanced techniques like cost-sensitive learning or ensemble methods specifically designed for extreme imbalance.

---

**A13. How would you deploy this system in a real bank?**

> Deployment would involve: (1) serialising the trained models using joblib or pickle into versioned model artifacts; (2) wrapping the preprocessing pipeline and prediction logic in a REST API (FastAPI or Flask); (3) containerising with Docker; (4) deploying behind a load balancer on the bank's private cloud or on-premises infrastructure; (5) connecting the Individual Risk Scanner UI to the API endpoint. The FERI computation is deterministic and requires no model call, so it can run client-side. Model retraining should be scheduled quarterly as new transaction data accumulates. A CI/CD pipeline would run the test suite before each model version promotion.

---

**A14. What would a production data pipeline look like compared to your current setup?**

> Our current setup generates synthetic data on demand from a script. A production pipeline would: (1) ingest real customer application data from the bank's CRM in near-real-time via Kafka or a database trigger; (2) apply the same preprocessing transformations via a stored pipeline artifact; (3) run FERI and model scoring; (4) log predictions to an audit database for regulatory reporting; (5) trigger alerts to compliance officers for Critical Risk scores; (6) feed aggregated FERI statistics to an RBZ reporting API quarterly. Data quality checks and schema validation would be added at ingestion to handle missing or malformed inputs.

---

**A15. How did you handle the test/train split to prevent data leakage?**

> We split the original 5,000-record dataset 80/20 using scikit-learn's train_test_split with stratify=y to preserve the class proportions in both splits. SMOTE was then applied only to the 4,000-record training portion. The scaler and encoder were fitted only on training data and applied (without re-fitting) to test data. Feature importance and model hyperparameters were selected using cross-validation on training data only. The test set of 1,000 records was set aside before any modelling began and accessed only for final evaluation reporting.

---

**A16. What is the F1-score mathematically? Why is it a harmonic mean rather than arithmetic mean?**

> F1 = 2 × (Precision × Recall) / (Precision + Recall). The harmonic mean penalises extreme imbalances between Precision and Recall more severely than an arithmetic mean. If Precision = 1.0 and Recall = 0.01, the arithmetic mean is 0.505 — suggesting a reasonable model. The harmonic mean gives 0.0198 — correctly reflecting that a model identifying almost nobody is not useful regardless of its precision. The harmonic mean ensures both components must be reasonably high for F1 to be high.

---

**A17. Logistic Regression had the best AUC but Random Forest had the best accuracy. How do you reconcile this?**

> ROC-AUC and accuracy measure different things. AUC is threshold-independent — it evaluates discriminative power across the entire operating range. Accuracy is evaluated at a single threshold (typically 0.5). A model can achieve higher AUC by better separating the score distributions of the two classes, while another model achieves higher accuracy by being better calibrated at the 0.5 threshold specifically. Logistic Regression produces well-calibrated probabilities because it directly optimises log-likelihood, giving it superior AUC. Random Forest's vote-aggregation tends to push probabilities toward 0.4–0.6, compressing its score distribution and depressing AUC, but its sharp 0.5-threshold classification is slightly better calibrated for accuracy.

---

**A18. Could you have used a neural network? What would you gain or lose?**

> A neural network with 2–3 hidden layers could potentially capture more complex non-linear interactions between features. However: (1) with 28 features and 5,092 training samples, a neural network would have more parameters than training samples per layer, requiring aggressive dropout regularisation and careful tuning; (2) neural networks do not natively provide feature importances, requiring post-hoc SHAP analysis; (3) they are computationally expensive for no demonstrated accuracy gain on structured tabular data at this scale — multiple academic benchmarks show XGBoost outperforming deep learning on structured tabular datasets with fewer than 100,000 samples; (4) for regulatory explainability, a neural network is significantly harder to justify to a compliance examiner.

---

**A19. What is the difference between bagging (Random Forest) and boosting (XGBoost)?**

> Bagging — Bootstrap Aggregating — trains multiple independent learners in parallel, each on a random bootstrap sample of the training data, and averages their predictions. Independence reduces variance. Random Forest is bagging over decision trees with random feature selection at each split. Boosting trains learners sequentially: each new model focuses on the errors of the combined previous ensemble, adjusting sample weights or training on residuals. Boosting reduces bias. Boosting models are typically more powerful but more prone to overfitting noisy data. For our dataset — which has clean, well-defined features from a calibrated generative process — both perform comparably, with XGBoost slightly lower AUC because its boosting mechanism captures some noise from the synthetic generation process.

---

**A20. What does StandardScaling do and which models need it?**

> StandardScaling transforms each continuous feature to zero mean and unit variance: z = (x - mean) / std. This is essential for Logistic Regression because the regularisation penalty (C parameter) applies uniformly across all coefficients — if features are on different scales, coefficients for large-magnitude features are penalised more aggressively, distorting the model. Tree-based models (Random Forest, XGBoost) are scale-invariant because splits are based on relative orderings, not magnitude. We apply scaling to all features for pipeline consistency, but it has a material effect only on Logistic Regression performance.

---

**A21. What is the AUC of a random classifier and what would AUC = 1.0 mean?**

> A random classifier — one that assigns probabilities independently of the features — achieves AUC = 0.5 because it has no discriminative power (the ROC curve follows the diagonal). AUC = 1.0 means the model perfectly separates excluded from included individuals: the lowest exclusion probability assigned to any truly excluded individual is higher than the highest probability assigned to any truly included individual. Our AUC of 0.849 means the model correctly ranks a random excluded individual above a random included individual 84.9% of the time.

---

**A22. Why did you not use the kyc_doc_score feature instead of individual document flags?**

> We included both. kyc_doc_score is the sum of the four individual document flags (0–4 range). Including individual flags alongside the aggregate score might seem redundant, but the individual flags allow models to identify differential effects: missing a National ID (40 FERI points) is categorically different from missing an Employment Proof (10 FERI points). The tree models automatically select the most discriminative split, and feature importance results confirm that has_national_id and has_proof_of_address rank above kyc_doc_score precisely because they capture the specific high-weight documents. The aggregate score loses this granularity.

---

**A23. How reproducible is your analysis?**

> Fully reproducible. We set random_state=42 in all stochastic operations: data generation, train/test split, SMOTE, Logistic Regression solver, Random Forest, and XGBoost. Running main.py twice on the same machine produces byte-identical output files. The only potential source of variation is Python library version differences, which we address through requirements.txt version pinning. The dataset is regenerated deterministically from the seed, so no external data file is required to reproduce the analysis.

---

**A24. What is the difference between the training, validation, and test sets in your pipeline?**

> Training set (80% of 5,000 = 4,000 records, SMOTE-expanded to 5,092): used to fit model weights and tree structures. Validation set (implicit, within cross-validation folds of the training set): used to select hyperparameters without touching test data. Test set (20% of 5,000 = 1,000 records, held out from the start): used once, only for final performance reporting. The test set has never been seen by the model during training or hyperparameter tuning, ensuring it provides an unbiased estimate of real-world performance.

---

**A25. What further work would improve the models?**

> Five directions: (1) Real microdata from the RBZ or a commercial bank's anonymised CRM would replace synthetic calibration with ground truth; (2) Adding time-series features — how long since the person last had a bank account, recent mobile money transaction volume — would increase predictive power; (3) Ensemble stacking of all three models using a meta-learner would typically add 1–2 AUC points; (4) Fairness-constrained training — optimising for equal recall across gender and location groups — would address potential discrimination; (5) Survival analysis modelling to predict not just whether someone is excluded but how long they have been excluded and when intervention is most effective.

---

## Section B — FERI Index (20 Questions)

---

**B1. How did you determine the FERI weights (45%, 35%, 20%)? Are they arbitrary?**

> The weights are theoretically grounded and cross-validated against our empirical results, though not statistically optimised through regression. They reflect three convergent sources: (1) FATF Recommendation 10 and the KYC literature, which consistently identifies documentation as the dominant formal onboarding barrier; (2) our Logistic Regression coefficients for the KYC document flags, which account for approximately 45% of the model's total coefficient weight; (3) a sensitivity analysis showing that varying weights by ±10% changes FERI scores by under 4 points and alters risk band assignments for fewer than 8% of individuals, confirming robustness. Future work using structural equation modelling with real microdata could yield empirically derived weights.

---

**B2. Why does National ID score 40 points in the KYC Gap sub-index — more than the other three documents combined?**

> National ID is the single document required by every regulated financial institution for every account type in Zimbabwe. Proof of Address is demanded for Tier 2 and above. TIN is required only for certain product types (credit, foreign exchange). Employment Proof is requested but sometimes waived. A person without a National ID cannot open any account, access mobile money formally, or use any supervised financial service. The 40-point weight reflects this absolute gating role — it is not merely one document among four, it is the prerequisite for all others.

---

**B3. Why is the FERI formula linear? Real exclusion risks might interact non-linearly.**

> The linear formula is a deliberate design choice for regulatory usability, not a limitation we overlooked. A non-linear formula (for example, one that multiplies rural and unemployed flags) would be harder for a bank compliance officer or RBZ examiner to interpret, audit, and justify in a compliance hearing. Composite indices in financial regulation — like the World Bank's Financial Development Index or the UNDP Human Development Index — are universally linear for this reason. The FERI is a policy communication tool. The ML models capture the non-linear interactions and confirm that the top-ranked risk groups identified by FERI align with the highest ML-predicted exclusion probabilities, validating the linear approximation.

---

**B4. What would happen to FERI scores if the RBZ introduced Tier 1 KYC? Would the index become obsolete?**

> Not obsolete — the index would need recalibration but would remain relevant. If Tier 1 onboarding removes the Proof of Address requirement, the 30-point PoA component would be zeroed for Tier 1 accounts, shifting the maximum KYC Gap score from 100 to 70 and reducing mean FERI scores across the population. The Demographic Vulnerability and Institutional Barrier sub-indices would still capture structural disadvantage for individuals who lack even a voter registration card. FERI would need annual recalibration against regulatory changes, which is standard practice for any composite index used in supervisory monitoring.

---

**B5. How does FERI compare to credit scoring systems like FICO or Experian?**

> Credit scores measure creditworthiness — the probability of loan default — based on repayment history, utilisation, and account age. FERI measures access risk — the probability of being structurally excluded from financial services — based on documentation gaps and structural disadvantage. Credit scores require prior financial history data that excluded individuals by definition do not have. FERI is specifically designed as a pre-onboarding tool: it identifies who is at risk of being turned away before they ever enter the credit system. It is conceptually closer to the World Bank's Financial Inclusion Index than to FICO.

---

**B6. The Institutional Barrier sub-index includes "distance to branch." Is this still relevant given mobile banking?**

> It remains relevant for two reasons. First, the analysis distinguishes mobile phone possession: individuals without a mobile phone cannot access mobile banking regardless of branch distance, and our dataset shows that 18% of the population lacks a mobile phone. For these individuals, branch distance remains a hard constraint. Second, even with a mobile phone, many banking products — mortgage origination, large cash deposits, certain account types — still require physical branch attendance in Zimbabwe's current regulatory environment. Distance matters for initial account opening even for digital-native accounts, as biometric verification and signature collection still occur in-branch for many institutions.

---

**B7. Why is "Female" a factor in the Demographic Vulnerability sub-index? Is that not discrimination?**

> The FERI index is a population-level risk assessment tool, not an individual discrimination instrument. Including gender as a risk factor reflects a documented statistical reality: FinScope Zimbabwe 2022 shows women are excluded at 5.6 percentage points higher than men, driven by structural barriers including address documentation linked to spouse's name, lower TIN registration rates due to informal sector concentration, and lower income quintile distribution. Capturing this reality in FERI enables targeted interventions for women — gender-responsive KYC guidance, shared-household address waivers — rather than ignoring the disparity. The FERI is intended to identify who needs policy support, not to determine who should be denied service.

---

**B8. Can two individuals with completely different profiles have the same FERI score?**

> Yes, and this is a known limitation of any composite index. A rural individual with all documents but no mobile phone and a distant branch could score the same as an urban individual without a National ID but close to a branch. The risk band classification at the aggregate level averages across such cases. This is why we recommend FERI as a segment-level supervisory tool — tracking the mean FERI of rural versus urban applicant pools — rather than as an individual-level decision gate. The Individual Risk Scanner presents the full sub-index breakdown alongside the composite score so that a compliance officer can see which specific barrier is driving the risk, not just the aggregate number.

---

**B9. How do you validate the FERI scores? Is there a ground truth?**

> We validate FERI through two mechanisms. First, face validity: higher FERI scores should correspond to higher actual exclusion rates in the data. Our results confirm this monotonically: Low Risk (mean FERI ~15) has 14% exclusion, Moderate Risk (~35) has 37%, High Risk (~55) has 62%, Critical Risk (~75) has 78%. Second, we correlate FERI with the ML-predicted exclusion probabilities: the Pearson correlation between FERI score and XGBoost exclusion probability is approximately 0.71, confirming the index captures similar information to the model while remaining interpretable. True external validation would require a prospective study tracking FERI-scored individuals' account opening outcomes.

---

**B10. Why four bands? Why not a continuous score with no bands?**

> A continuous score is ideal for statistical analysis but impractical for regulatory communication and operational decision-making. Bands provide actionable categories: a compliance team can be trained to apply a specific intervention protocol (Tier 1 form, community vouching referral, agent banking referral, emergency outreach) based on the band, without needing to interpret a specific score of 47.3 vs 51.8. Four bands also align with FATF's CDD tier structure and with our policy recommendations, creating a direct mapping between risk score and prescribed regulatory response.

---

**B11. What happens to the FERI score if a person has all four documents?**

> If all four documents are held, the KYC Gap score is zero. The person's FERI is then entirely determined by Demographic Vulnerability and Institutional Barrier sub-indices. A fully documented rural unemployed person with no mobile phone and 50km to the nearest branch would still score approximately 0.35 × (20+20+15) + 0.20 × (30+20+30) = 0.35×55 + 0.20×80 = 19.25 + 16 = 35.25, placing them in the Moderate Risk band despite full documentation compliance. This correctly captures that documentation alone does not eliminate exclusion for individuals facing severe institutional and demographic barriers.

---

**B12. Is the FERI index your original contribution or does it build on existing indices?**

> The specific FERI formula, weights, band thresholds, and sub-index components are our original contribution developed for this study. It draws conceptually on: the World Bank Financial Inclusion Database composite methodology, the UNDP Human Development Index's weighted sub-index structure, and the Financial Action Task Force's risk-proportionate KYC framework. To our knowledge, no prior study in the Zimbabwean financial inclusion literature has constructed a composite KYC-barrier-specific index at the individual level. The existing literature uses FinScope survey statistics descriptively rather than modelling individual-level risk scores.

---

**B13. Could the FERI weights be derived empirically using regression?**

> Yes. A structural equation model with real bank application outcome data (approved/denied) as the dependent variable and sub-index components as predictors could produce statistically optimised weights. Alternatively, an optimization problem could be set up to maximise the correlation between FERI and the ML-predicted exclusion probability, using gradient descent to find the weights that minimise the squared difference. We did not pursue this because: (1) we lack real outcome data; (2) empirically derived weights from our synthetic data would be circular (we would be optimising a composite to match a model trained on the same synthetic data); (3) theoretically grounded weights are more defensible in a regulatory submission than black-box optimised ones.

---

**B14. What is the mean and standard deviation of FERI in your population?**

> Mean FERI: 30.83. Median: 28.77. Standard deviation: 19.25. The distribution is right-skewed, with the bulk of the population in the Low and Moderate Risk bands and a long tail into High and Critical Risk. The skewness reflects the real population structure: the majority of Zimbabweans have at least a National ID and are urban or peri-urban, while a minority face compound disadvantage across all three sub-indices simultaneously.

---

**B15. How would the FERI of the population change if National ID coverage increased to 95%?**

> Currently 78% of the synthetic population holds a National ID, and missing it contributes 40 points to the KYC Gap. If coverage rises to 95%, approximately 850 additional individuals (17% of 5,000) would have their KYC Gap score reduced by 40 points, reducing their FERI by 0.45 × 40 = 18 points. This would shift a substantial portion of the High Risk band into Moderate Risk. The population mean FERI would fall from approximately 30.8 to approximately 27.3 — a 3.5-point reduction. This single intervention — ensuring universal National ID coverage — would be the most impactful single change to population FERI scores.

---

**B16. Is the FERI Institutional sub-index capturing demand-side or supply-side barriers?**

> Supply-side barriers: branch distance is a supply constraint (the bank has not placed infrastructure near the individual), mobile phone absence is partly a supply/affordability constraint (network coverage and device cost), and internet access absence similarly reflects infrastructure provision and cost. The Demographic sub-index captures more demand-side factors: income, employment, education. The distinction matters for policy: supply-side barriers are addressed by provider mandates (agent banking requirements, mobile network rollout); demand-side barriers require income support, financial literacy, and document regularisation programs.

---

**B17. What is the highest possible FERI score and what profile would achieve it?**

> The theoretical maximum is 100. The maximum KYC Gap is 100 (all four documents missing): 0.45 × 100 = 45. The maximum Demographic Vulnerability is 103 (all factors present): capped at 100 for the sub-index. Applying the 35% weight: 0.35 × 100 = 35. The maximum Institutional Barrier is 100 (all factors present): 0.20 × 100 = 20. Total maximum: 45 + 35 + 20 = 100. The profile achieving this would be: rural, female, unemployed, no education, income Q1, age under 25 or over 64, no National ID, no Proof of Address, no TIN, no Employment Proof, no mobile phone, no internet, over 20km from branch, in a remote province. In practice, our maximum observed FERI in the dataset is approximately 88, because the probability of every single factor being simultaneously true is low.

---

**B18. Why did you include Age 65+ in the Demographic Vulnerability sub-index?**

> Older individuals in Zimbabwe face compounded documentation barriers: ID cards issued decades ago may have expired or been lost, proof of address documents may be in a deceased spouse's name, and TIN registration is lower among pensioners who withdrew from formal employment before the TIN system was widely implemented. Additionally, digital literacy and mobile banking adoption rates drop sharply above age 65, amplifying institutional barriers. FinScope Zimbabwe 2022 shows the 65+ group has lower formal account ownership than the 26–64 age group despite longer exposure to financial services.

---

**B19. How does FERI handle individuals in informal employment differently from unemployed individuals?**

> Informally employed individuals score 12 points in the Demographic Vulnerability sub-index; unemployed individuals score 20 points. This differential reflects their different documentation risk profiles. An informally employed person — a market trader, domestic worker, or subsistence farmer — typically lacks an Employment Proof document but may have some income and mobile money access. An unemployed individual faces both the documentation gap and the income constraint simultaneously, which is more severely correlated with exclusion in the FinScope data (70% exclusion vs 56% for informal employment). The Institutional and KYC sub-indices then add additional differentiation based on each individual's specific situation.

---

**B20. Could the FERI be applied to other African countries?**

> The formula structure is transferable; the specific weights and thresholds require recalibration. The three sub-index categories — documentation gap, demographic vulnerability, institutional barriers — are universal to African financial inclusion contexts. However, the specific documents weighted in the KYC Gap sub-index reflect Zimbabwe's regulatory requirements. In Kenya, for example, the National ID has near-universal coverage, so proof of address and M-Pesa registration dominate the documentation barrier. In Nigeria, the Bank Verification Number (BVN) system changes the documentation architecture entirely. A country-specific FERI would require: (1) identifying the mandatory documents for each regulatory tier; (2) weighting by exclusion impact as measured by that country's national financial inclusion survey; (3) recalibrating band thresholds against the national exclusion distribution.

---

## Section C — KYC / Financial Regulation (20 Questions)

---

**C1. What is KYC and what laws mandate it in Zimbabwe?**

> Know Your Client is a regulatory compliance process requiring financial institutions to verify customer identity before establishing a business relationship or conducting transactions. In Zimbabwe it is mandated by: the Bank Use Promotion and Suppression of Money Laundering Act (Chapter 24:24), the Money Laundering and Proceeds of Crime Act (Chapter 9:24), and RBZ Directive 01-2017 on Customer Due Diligence. These laws transpose Zimbabwe's obligations under the Eastern and Southern Africa Anti-Money Laundering Group (ESAAMLG) and the Financial Action Task Force 40 Recommendations. Non-compliance exposes institutions to licence suspension and AML fines.

---

**C2. What is FATF and what is Recommendation 10?**

> The Financial Action Task Force is the intergovernmental body that sets global standards for combating money laundering, terrorist financing, and proliferation financing. It has 40 Recommendations. Recommendation 10 specifically addresses Customer Due Diligence, requiring that financial institutions identify and verify customer identity using reliable, independent source documents or data. Critically, Recommendation 10 explicitly allows a risk-proportionate approach: where risks are lower — small accounts, low-value transactions, specific customer types — simplified CDD measures are permitted. Zimbabwe is an ESAAMLG member and an FATF-observing jurisdiction, meaning it is assessed against the 40 Recommendations in mutual evaluation reviews.

---

**C3. What is the difference between CDD and EDD?**

> CDD — Customer Due Diligence — is standard identity verification required for all customers: identity document, address verification, nature of business or employment. EDD — Enhanced Due Diligence — applies to higher-risk customers: Politically Exposed Persons (PEPs), customers from high-risk jurisdictions, high-value transactions above reporting thresholds. EDD requires source-of-funds documentation, senior management approval, and ongoing enhanced monitoring. Our study focuses on the CDD tier — the standard onboarding requirement — because it is the barrier encountered by ordinary citizens seeking basic savings accounts.

---

**C4. What is the Reserve Bank of Zimbabwe's role in financial inclusion?**

> The RBZ is Zimbabwe's central bank and primary financial sector regulator. It licenses banks, building societies, microfinance institutions, and money transfer operators. It issues KYC compliance directives, publishes the National Financial Inclusion Strategy (NFIS), and supervises the Financial Intelligence Unit. The NFIS 2022–2026 targets reducing financial exclusion to below 30% by 2027, increasing formal savings account ownership, and expanding mobile financial services in rural areas. The RBZ also chairs the Financial Inclusion Taskforce, which coordinates across government ministries, mobile network operators, and civil society.

---

**C5. What is a Politically Exposed Person (PEP) and how does that relate to your study?**

> A PEP is an individual who holds or has held a prominent public function: heads of state, senior government officials, senior judicial or military officials, senior executives of state-owned enterprises, and their family members and close associates. PEPs present elevated money laundering risk due to potential corruption exposure. Banks are required to apply EDD to PEPs, including source-of-funds documentation and senior management approval. Our study focuses on the opposite end of the risk spectrum: low-income, rural, and informal sector individuals who pose low AML risk but face identical or greater documentation barriers to account opening.

---

**C6. What is the Financial Intelligence Unit in Zimbabwe?**

> The Financial Intelligence Unit (FIU) is a government body established under the Money Laundering and Proceeds of Crime Act. It receives, analyses, and disseminates financial intelligence — including Suspicious Transaction Reports from financial institutions — to law enforcement. Our study recommends that the FIU also receive quarterly FERI-banded rejection rate reports from regulated institutions, expanding its role from purely receiving suspicious activity reports to monitoring inclusion metrics. This mirrors the role of South Africa's Financial Intelligence Centre and Kenya's Financial Reporting Centre, which publish both AML compliance metrics and financial inclusion progress reports.

---

**C7. Why does proof of address specifically exclude rural populations?**

> Proof of address in Zimbabwe's formal banking context typically means a utility bill (ZESA electricity, water bill), a bank statement at a physical address, or a lease agreement. Rural areas in Zimbabwe have low formal utility coverage: communal land is not serviced by ZESA in the same way as urban plots, piped water is not metered at household level, and communal farmers do not hold lease agreements on customary land. This means the specific documents that constitute acceptable proof of address in the regulatory framework are structurally unavailable to rural populations regardless of their actual residence. Alternative documentation — chief's letters, GPS coordinates, mobile network location data — exists but lacks legal standing without an explicit RBZ directive.

---

**C8. What is the FinScope Consumer Survey and how is it used in policy?**

> FinScope is a standardised nationally representative household survey instrument developed by FinMark Trust, a South African non-profit funded by the UK Foreign Commonwealth and Development Office. It has been conducted in over 20 African countries with comparable methodology. The Zimbabwe 2022 edition interviewed approximately 5,000 adults using stratified random sampling across all provinces. Results feed directly into the RBZ's National Financial Inclusion Strategy targets, the World Bank Financial Inclusion Database, and ESAAMLG's regional financial integrity assessments. It is the authoritative source for Zimbabwe financial inclusion statistics.

---

**C9. What is agent banking and why is it relevant to your recommendations?**

> Agent banking allows licensed financial institutions to deliver banking services through retail agents — shops, mobile money kiosks, post offices — rather than traditional branches. The agent uses a mobile POS terminal connected to the bank's system to conduct account opening, deposits, and withdrawals on behalf of the bank. RBZ regulations permit agent banking under certain conditions but penetration remains low in rural areas. Our FERI Institutional sub-index penalises individuals in areas distant from any financial service point. Mandating minimum agent banking density in underserved districts — a direct regulatory intervention — would reduce the institutional barrier sub-index for the rural Critical Risk band.

---

**C10. What is EcoCash and how does its KYC differ from formal banking KYC?**

> EcoCash is Econet Wireless Zimbabwe's mobile money platform, the dominant mobile financial service in Zimbabwe with over 7 million registered users. EcoCash operates under RBZ's National Payments System regulation and applies simplified KYC: a single National ID is sufficient to open a Tier 1 EcoCash wallet. This is the FATF-compliant simplified CDD in practice. However, EcoCash wallets have transaction limits, cannot be used for mortgage applications, do not build a credit score, and do not satisfy the full banking requirements for payroll accounts. Our study recommends formalising EcoCash transaction history as supplementary KYC evidence for banks wishing to upgrade a mobile money user to a formal bank account.

---

**C11. What is de-risking and how does it worsen exclusion?**

> De-risking is when financial institutions exit entire customer segments, business lines, or correspondent banking relationships rather than managing the compliance risk of serving them. Banks may refuse to serve money transfer operators, microfinance institutions, or NGOs in high-risk jurisdictions because the compliance cost of AML monitoring exceeds the commercial return. This has been documented as a significant secondary cause of financial exclusion in Southern Africa: if a bank decides that informal sector customers present too much AML risk relative to the KYC verification cost, it withdraws from that market, excluding the entire segment regardless of individual risk. Our tiered KYC recommendation reduces per-customer compliance cost for low-risk segments, making de-risking economically irrational for Tier 1 accounts.

---

**C12. How does the RBZ National Financial Inclusion Strategy 2022–2026 relate to your work?**

> The NFIS 2022–2026 sets specific quantitative targets: reducing financial exclusion from 38% to below 30% by 2027, increasing the proportion of adults with formal savings from 22% to 35%, and extending agent banking to all district centres. Our study directly supports the NFIS evidence base by providing the first quantitative machine learning analysis of which KYC barriers are most responsible for the current 38% exclusion rate. Our six policy recommendations align with NFIS strategic pillars: simplified onboarding (Tier 1 KYC), digital identity (NFIS Pillar 3), rural access (Pillar 2), and gender inclusion (Pillar 4).

---

**C13. What is mobile money regulation in Zimbabwe and how is it structured?**

> Mobile money in Zimbabwe is regulated under the National Payments System Act (Chapter 24:23) and RBZ's National Payments System Framework. Mobile money operators — EcoCash (Econet), OneMoney (NetOne), Telecash (Telecel) — require an RBZ licence to operate. They are subject to simplified KYC requirements for Tier 1 wallets (ID only, transaction limits of USD 500/month) and full CDD for higher-tier products. The RBZ has the authority to adjust these tiers without new legislation, which is relevant to our recommendation for mobile-first onboarding — it could be implemented through a regulatory directive rather than a parliamentary amendment.

---

**C14. What would a Tier 1/2/3 KYC framework look like in practice for Zimbabwe?**

> Tier 1 (Basic Account): National ID or voter registration card only. Monthly transaction limit of USD 500. Eligible for mobile money, basic savings, and payment accounts. No proof of address, no TIN, no employment proof. Tier 2 (Standard Account): National ID plus one corroborating document (employer letter, community leader attestation, utility bill, mobile network location confirmation). Monthly limit of USD 5,000. Eligible for credit products, payroll accounts, and foreign exchange access up to regulated thresholds. Tier 3 (Full CDD): All four documents plus source-of-funds declaration for accounts above USD 10,000 monthly turnover. Full range of banking products. This mirrors the tiered frameworks implemented in Kenya (2017), Tanzania (2016), and Nigeria (2013) under their respective central bank directives.

---

**C15. Could criminalising over-compliance be a useful regulatory tool?**

> This is an emerging regulatory approach in some jurisdictions. The UK Financial Conduct Authority has issued guidance warning banks that refusing legitimate business on vague AML grounds is itself a regulatory risk — institutions can face sanctions for unjustified de-risking. In Zimbabwe, the RBZ could similarly issue compliance guidance clarifying the minimum acceptable documentation set and stating explicitly that demanding documentation beyond the minimum for Tier 1 accounts constitutes non-compliance with the Bank Use Promotion Act's financial inclusion mandate. This shifts the regulatory incentive: over-compliance with AML requirements becomes a compliance risk in its own right, balancing it against the under-compliance risk.

---

**C16. What is the difference between financial exclusion, financial underservice, and financial inaccessibility?**

> Financial exclusion means having no formal financial account of any kind — no bank account, no mobile money wallet, no insurance policy. Financial underservice means having an account but not using financial services that would be economically beneficial — for example, holding a mobile money wallet but not accessing credit, insurance, or savings products because they require documentation the individual lacks. Financial inaccessibility is the supply-side condition — services exist but physical or digital access barriers prevent their use. Our study primarily models financial exclusion (the binary target variable) but the FERI index captures both inaccessibility (Institutional sub-index) and vulnerability factors that drive underservice.

---

**C17. Why is the TIN required by banks and who issues it in Zimbabwe?**

> The Tax Identification Number is issued by the Zimbabwe Revenue Authority (ZIMRA) to individuals and entities for tax registration purposes. Banks require TINs for accounts above certain thresholds and for all corporate accounts to facilitate ZIMRA's interest income reporting obligation. Many informal sector workers, subsistence farmers, and unemployed individuals have never registered with ZIMRA and therefore do not hold a TIN. Obtaining a TIN requires a National ID, proof of address, and often proof of income — creating a documentation cascade where lacking one document prevents obtaining another.

---

**C18. What is the role of microfinance institutions in Zimbabwe's financial inclusion landscape?**

> Microfinance institutions (MFIs) operate under the Microfinance Act (Chapter 24:29) and are licensed by the RBZ. They provide credit to small and medium enterprises and individuals excluded from commercial banking, using alternative collateral (group guarantees, savings history) rather than formal asset documentation. MFIs typically apply lighter KYC requirements than commercial banks. However, most MFIs operate in urban and peri-urban areas and their interest rates (often 30–50% per annum) limit access for the lowest-income segments. Our study recommends that MFI loan history be recognised as financial track record evidence in commercial bank KYC, creating a formal pathway from microfinance to mainstream banking.

---

**C19. What is the African Continental Free Trade Area's relevance to KYC harmonisation?**

> The AfCFTA, which Zimbabwe ratified in 2019, aims to create a unified African market including financial services. A harmonised pan-African KYC framework — a common set of acceptable identity documents and verification standards — would reduce the compliance cost of cross-border payments and correspondent banking significantly. The African Union's Inter-African Bureau for Financial Affairs (AFRITAC) is working on minimum KYC standards that would apply across member states. A national digital ID that is SADC-interoperable, as our recommendation proposes, would position Zimbabwe for this regional harmonisation and reduce remittance compliance costs for the Zimbabwean diaspora.

---

**C20. What is the difference between AML and KYC?**

> AML — Anti-Money Laundering — is the broader regulatory framework covering all measures to prevent financial system use for laundering criminal proceeds: transaction monitoring, suspicious activity reporting, correspondent bank due diligence, and sanctions screening. KYC — Know Your Client — is one component of AML: the customer identity verification process at account opening and on an ongoing basis. KYC provides the customer identity baseline from which AML transaction monitoring operates. Without knowing who the customer is, anomalous transaction patterns cannot be attributed. Our study focuses specifically on KYC because it is the onboarding barrier, not the transaction monitoring barrier, that causes exclusion.

---

## Section D — Zimbabwe Economic Context (15 Questions)

---

**D1. What caused the 2007–2009 Zimbabwean hyperinflation and how does it relate to financial exclusion today?**

> The hyperinflation — peaking at an officially estimated 89.7 sextillion percent in November 2008 — was caused by: the Reserve Bank of Zimbabwe printing money to fund government deficits, compounded by land reform's destruction of agricultural export revenue, international sanctions reducing foreign currency inflows, and political instability deterring investment. The banking sector collapsed as savings were wiped out overnight. Many citizens withdrew entirely from formal banking and have not re-engaged. Those who exited in 2007–2009 are now 15–20 years older: their address documents from that era have expired, their TINs (if they had them) are deregistered, and their banking relationships with now-defunct institutions are undocumented. This creates a structural cohort of individuals who face re-entry barriers that our model captures through age and documentation gap interactions.

---

**D2. What is the current Zimbabwean currency situation and does it affect KYC compliance?**

> Zimbabwe has had a complex currency history: the original Zimbabwean dollar was abandoned in 2009 in favour of the multi-currency system using US dollars, South African rand, and others. The RTGS dollar / Zimbabwe dollar was reintroduced in 2019 and has faced continued depreciation. In 2024, the ZiG (Zimbabwe Gold) currency was introduced. The multi-currency environment creates KYC complications: bank accounts can be denominated in USD or ZiG, with different documentation requirements and reporting thresholds. Currency instability also depresses savings motivation — holding money in a depreciating currency in a formal account is economically irrational, reducing formal account utilisation among lower-income segments even when they have accounts.

---

**D3. What is the Zimbabwe rural/urban split and why does it matter for your analysis?**

> Approximately 67% of Zimbabwe's population lives in rural areas (World Bank 2023), with urban concentration in Harare, Bulawayo, and Mutare. Our synthetic dataset reflects a 44/56 rural/urban split derived from FinScope 2022, which sampled urban areas at higher rates. Rural financial exclusion at 61% versus urban 17% represents the study's most dramatic finding. The gap is driven by: lower National ID possession (many rural residents were registered during the 2018 biometric ID rollout but some remote areas had incomplete coverage), near-zero proof of address document availability, greater distance from any financial service point, and lower education levels reducing financial literacy and document awareness.

---

**D4. Which provinces are most financially excluded in Zimbabwe?**

> Based on FinScope Zimbabwe 2022, the most financially excluded provinces are Matabeleland North (67% excluded), Matabeleland South (62%), and Mashonaland Central (58%). These provinces have the lowest formal employment rates, highest dependence on subsistence agriculture, greatest distances from branch infrastructure, and — in the Matabeleland provinces — historical tensions with central government institutions that have reduced engagement with formal services. Harare (12% excluded) and Bulawayo (18% excluded) are the least excluded. Our synthetic dataset replicates this provincial distribution using FinScope's published provincial estimates.

---

**D5. How does Zimbabwe's high unemployment rate affect financial exclusion and your model?**

> Zimbabwe's formal unemployment rate is estimated at 5–7%, but this masks a much higher effective non-employment rate: approximately 70% of working-age Zimbabweans are in informal employment (subsistence farming, vending, domestic service, cross-border trading). Informally employed individuals lack employment proof documents, payslips, or formal employer letters. Our model shows unemployed individuals face a 46.6% exclusion rate — lower than FinScope's 70% target, which we acknowledge as our largest calibration discrepancy. The discrepancy arises because our independent marginal generation of urban/rural and employment attributes does not fully capture the real compounding: rural + unemployed + no education in Zimbabwe has a higher joint exclusion probability than independent marginals would predict.

---

**D6. What is the relationship between education level and financial exclusion in your findings?**

> Education is a significant predictor in all three models. Individuals with no formal education have a 59.6% exclusion rate and mean FERI of 46.6, compared to 21.5% exclusion and FERI of 21.8 for tertiary educated individuals. The mechanism is multi-channel: education increases the probability of formal employment (and thus employment proof), increases income (moving up quintiles), increases digital literacy (improving mobile banking adoption), and increases awareness of documentation requirements and how to obtain them. In our feature importance results, education_level ranks fourth or fifth across models, behind document possession flags but ahead of province and gender.

---

**D7. How does Zimbabwe's land reform relate to proof of address barriers?**

> The Fast Track Land Reform Programme (2000–2002) resettled hundreds of thousands of individuals onto former commercial farm land under customary or A1 scheme tenure. These resettled individuals hold land occupation rights but not title deeds. Their address documentation is typically a letter from the local village committee or a plot allocation document that is not accepted by formal banks. The result is that a population segment created by a government land redistribution policy is simultaneously denied banking access because their government-issued land documentation does not meet the banking regulator's proof of address standard — a direct policy contradiction that our recommendations address.

---

**D8. What is the gender gap in financial exclusion specifically in the Zimbabwean context?**

> FinScope Zimbabwe 2022 records 43% female exclusion versus 33% male exclusion — a 10 percentage-point gap. Our model generates a smaller gap (38.9% vs 33.7%) due to calibration constraints. The primary mechanisms behind the real gap are: (1) proof of address documents (utility bills, lease agreements) are typically registered in the male head of household's name — women in shared households cannot produce address documentation in their own name; (2) TIN registration rates are lower for women in informal employment; (3) lower income quintile representation, with women over-represented in Q1 and Q2; (4) lower National ID possession rates in rural areas, where women's ID registration was historically lower and is improving but incomplete. Our gender-responsive KYC recommendation directly targets mechanism (1).

---

**D9. How does the informal economy affect your analysis?**

> Zimbabwe's informal economy is estimated at 60–80% of GDP depending on the measurement methodology. Informal sector workers — market traders, small-scale miners, domestic workers, subsistence farmers — are typically in cash-based transactions, have no payslips, may lack TINs, and rotate addresses seasonally. Our Employment Proof flag captures formal-sector employment certification, and 54% of the dataset is informally employed. The informal sector concentration is a key reason our overall exclusion rate (36.4%) is slightly below the FinScope target (38%) — informal workers who do hold a National ID can achieve partial financial access through mobile money even without proof of address, reducing their model-predicted exclusion probability below what the true structural barriers might suggest.

---

**D10. What is ESAAMLG and how does Zimbabwe fit into it?**

> ESAAMLG — the Eastern and Southern Africa Anti-Money Laundering Group — is an FATF-style regional body covering 18 countries including Zimbabwe, Zambia, Tanzania, Kenya, South Africa, and others. It conducts mutual evaluation reviews assessing each member's AML/CFT compliance against the FATF 40 Recommendations. Zimbabwe's last mutual evaluation was in 2016, with a follow-up assessment in 2022. ESAAMLG evaluations influence correspondent banking relationships and donor funding availability — a poor rating can lead to de-risking by international banks. Our recommendations are designed to be ESAAMLG-compliant: the Tier 1 framework specifically cites FATF Recommendation 10's risk-proportionate provision.

---

**D11. What mobile money penetration statistics did you use and where from?**

> FinScope Zimbabwe 2022 reports 52% of adults have an active mobile money account. Our dataset reflects this through the has_mobile_phone binary flag (82% possession) combined with actual mobile money registration patterns. EcoCash's 2023 annual report cited 7.9 million registered subscribers in a population of approximately 15.9 million adults — consistent with FinScope. Mobile money penetration is higher in urban areas (92%) and lower in rural areas (65%), reflecting network coverage, device affordability, and literacy constraints. The 18% of our population without a mobile phone — concentrated in the Critical Risk band — are entirely excluded from the mobile-first onboarding alternative.

---

**D12. How does brain drain affect financial exclusion in Zimbabwe?**

> Zimbabwe's skilled emigration — estimated at 3–4 million Zimbabweans in South Africa, the UK, the US, and Australia — has two countervailing effects on domestic financial exclusion. On one hand, remittances from the diaspora support income in Q1 and Q2 households, potentially raising their FERI Demographic sub-index. On the other hand, brain drain depletes formal employment in the domestic economy, reducing the size of the formally employed class that holds full documentation suites, and concentrating formal sector employment in Harare and Bulawayo. The domestic formal banking sector's human capital constraints also slow the development of digital onboarding solutions that could reduce KYC barriers.

---

**D13. What is the Bank Use Promotion Act and what does it say about inclusion?**

> The Bank Use Promotion and Suppression of Money Laundering Act (Chapter 24:24) was originally enacted to encourage use of the formal banking system during the hyperinflation era when businesses were holding cash outside banks. It empowers the RBZ to issue directives on minimum account conditions, reporting requirements, and KYC standards. Section 14 gives the RBZ broad regulatory authority to prescribe conditions for account opening. Our recommendations are framed as directives under Section 14 rather than requiring new legislation — the RBZ already has the legal authority to implement tiered KYC, alternative proof of address acceptance, and FERI reporting requirements through a compliance bulletin.

---

**D14. How does climate vulnerability interact with financial exclusion in rural Zimbabwe?**

> Zimbabwe experiences recurrent drought, flood, and cyclone impacts — Cyclone Idai (2019) and El Nino droughts (2023–2024) have devastated rural agricultural communities. Climate shocks destroy documentation: ID cards, bank books, and address papers are lost in floods. They also destroy informal savings (cattle, grain) that rural households use as economic buffers. This creates acute spikes in financial exclusion following climate events, with affected individuals needing rapid financial access precisely when their documentation is most incomplete. A digital identity system that does not depend on physical document possession — as recommended — would be resilient to climate disruption in a way that paper-based KYC is not.

---

**D15. What does your study contribute that existing Zimbabwean financial inclusion research has not?**

> Existing research in Zimbabwe — including World Bank Financial Sector Assessment Programme reports, RBZ NFIS progress reviews, and academic papers in the Southern Africa Journal of Finance — uses FinScope data descriptively: presenting cross-tabulations and identifying which groups are excluded. Our study makes four contributions that go beyond this: (1) we model individual-level exclusion probability using supervised machine learning, producing a predictive tool rather than a retrospective description; (2) we quantify the relative importance of each barrier through feature importance and SHAP analysis, identifying National ID and Proof of Address as the dominant drivers rather than income or location; (3) we develop the FERI composite index as a regulatory monitoring tool that did not previously exist; (4) we build a deployable interactive platform that makes these findings accessible to non-technical bank compliance officers and RBZ supervisors.

---

## Section E — Ethics, Bias & Research Integrity (10 Questions)

---

**E1. Is it ethical to build a model that predicts whether someone will be financially excluded?**

> Ethical concerns depend entirely on how the model is used. A model that identifies systemic exclusion patterns for policy intervention — which is our intended use — is ethically affirmative: it reveals injustice and guides remediation. A model used to screen individual applicants for account denial would be ethically problematic: it would perpetuate structural disadvantage by using historical exclusion patterns to justify future exclusion. We have explicitly designed the system to be a policy tool and a compliance officer support tool, not an account approval engine. The FERI scanner recommends interventions (which documents to help the customer obtain, which agent banking channel to direct them to) rather than approve/deny decisions.

---

**E2. Does your model reproduce historical discrimination?**

> The model is trained on synthetic data that reflects the real Zimbabwean exclusion distribution, which includes historical and structural discrimination against women and rural populations. Including gender and location as features means the model will — accurately — show that women and rural individuals face higher exclusion risk. This reflects reality, not model bias. However, using this model's output to make individual loan decisions would constitute disparate impact discrimination under most legal frameworks. We acknowledge this limitation explicitly and recommend that any operational deployment include a fairness audit examining whether the model's predictions have disparate impact across gender, location, and income quintile groups.

---

**E3. What are the limitations of synthetic data for policy research?**

> Four key limitations: (1) synthetic data cannot capture complex household dynamics — inter-generational sharing of documents, informal credit relationships, seasonal migration — that influence real exclusion; (2) independent marginal distributions do not fully capture joint probabilities, particularly for compounded disadvantage (rural + unemployed + female + no education); (3) calibration is only as good as the source survey — FinScope's sampling methodology may underrepresent the most excluded populations who are hardest to survey; (4) the synthetic data does not evolve — it is a static 2022 snapshot that does not reflect post-2022 changes in the regulatory environment, mobile money penetration, or economic conditions.

---

**E4. How did you address the risk of FERI being misused as a credit denial tool?**

> By design and documentation. First, the dashboard's Individual Risk Scanner explicitly labels outputs as "Risk Assessment for Intervention Planning" not "Account Approval Score." Second, the VIVA paper and policy recommendations section explicitly state that FERI scores should not be used in individual credit decisions and must not appear in bank credit scoring models without a regulatory fairness audit. Third, we recommend that FERI use in supervisory reporting be at the aggregate segment level — mean FERI of rejected applications by demographic — not at the individual level. The distinction between a population monitoring tool and an individual decision tool is fundamental to our system design.

---

**E5. Is your study replicable? How would another researcher reproduce your results?**

> Fully replicable. The complete source code is available in the repository. Running python main.py with seed=42 produces byte-identical outputs. The data generation function uses only standard probability distributions (scipy, numpy) from published FinScope statistics. No proprietary data, licensed software, or institutional access is required. The requirements.txt file pins all library versions. A researcher with Python 3.10+ and pip can reproduce all figures, model metrics, and FERI statistics in under 60 seconds on a standard laptop. This full reproducibility is a core research integrity commitment of our study.

---

**E6. Did you consider privacy implications of your dataset?**

> Our dataset is entirely synthetic — it contains no real individuals, no real names, no real ID numbers. Privacy is not a concern for the dataset itself. If this framework were applied to real bank customer data, stringent privacy protections would be required: data minimisation (only collect what is needed for FERI computation), purpose limitation (FERI scores computed for regulatory reporting cannot be used for commercial targeting), data subject rights under Zimbabwe's Data Protection Act, and technical controls (encryption of individual scores, access logging). The synthetic dataset approach was partly chosen to avoid these complications in an academic research context.

---

**E7. How did your group ensure the analysis was balanced and not politically motivated?**

> Our study is technically anchored to published statistics and reproducible code, not to political positions. Our findings — that documentation requirements drive exclusion — are consistent with World Bank and FinMark Trust research across multiple African countries and do not depend on any political interpretation. Our policy recommendations are framed within the existing regulatory framework (FATF, RBZ NFIS, Bank Use Promotion Act) and explicitly cite legal instruments for each recommendation. We acknowledge the study's limitations including synthetic data and calibration gaps, which prevents overclaiming. The supervisor, Ms Bridget Munyoro, reviewed the methodology and findings throughout the project.

---

**E8. What would constitute research misconduct in a study like this?**

> Potential misconduct would include: (1) presenting synthetic data as if it were real survey microdata without disclosure; (2) cherry-picking model performance metrics (reporting only AUC and not F1, which is lower); (3) adjusting calibration targets post-hoc to make the model look better; (4) overstating policy implications beyond what the data supports; (5) failing to disclose limitations. Our study addresses all five: we clearly label the data as synthetic throughout, report all five metrics for all three models, publish the calibration verification output including the 13pp discrepancy in unemployed exclusion, explicitly limit policy recommendations to suggestions rather than conclusions, and dedicate a full limitations section to calibration gaps and data constraints.

---

**E9. How did you divide work among the three group members?**

> Knowledge Keche led the literature review, data generation design, and policy recommendations chapter. Lennie Dube designed and implemented the preprocessing pipeline, model training scripts, FERI formula, and the feri.py module. Jonah Chigaba implemented the Streamlit dashboard, visualisation module, and results analysis. All three members contributed to Chapter 3 (Methodology) and Chapter 4 (Results). Code reviews were conducted jointly using Git version control. The main.py pipeline integrates all three modules and was developed collaboratively.

---

**E10. If a reviewer asked you to improve the study with one additional analysis, what would you add?**

> We would add a counterfactual policy simulation: using the trained models and FERI formula, simulate the effect of each policy recommendation individually and in combination. For example: set has_proof_of_address = 1 for all rural individuals (simulating universal acceptance of chief's letters) and recompute the population's mean exclusion rate and mean FERI. Repeat for each recommendation. This would allow us to rank the six policies by estimated exclusion rate reduction, giving regulators a cost-effectiveness ordering. The simulation is technically feasible with our existing codebase — it requires only a parameter sweep across the FERI inputs — and would significantly strengthen the policy relevance of the study.

---

## Section F — Presentation-Day Tips

**Know cold — no looking at notes for these:**
- AUC: LR 0.849, RF 0.843, GB 0.832
- Accuracy: LR 77.2%, RF 77.4%, GB 76.8%
- F1: LR 0.700, RF 0.698, GB 0.663
- Training samples: 5,092 (post-SMOTE, balanced)
- Test samples: 1,000 (original distribution)
- Features: 28 (after One-Hot Encoding)
- Rural exclusion: 61.0% | Urban: 16.9% | Gap: 44pp
- Income Q1 exclusion: 65.6% | Q5: 11.8%
- Mean FERI: 30.83 | Std: 19.25 | Median: 28.77
- Critical Risk band: 4.5% of population, ~78% exclusion
- FERI formula: 0.45 × KYC + 0.35 × Demographic + 0.20 × Institutional
- FERI bands: 0–25 Low, 25–45 Moderate, 45–65 High, 65–100 Critical
- FinScope 2022 target: 38% exclusion nationally
- NFIS target: below 30% by 2027

**When under pressure:**
- Pause, breathe, then answer.
- "That is a nuanced question. To be precise..." buys 3 seconds.
- "Our study specifically addresses X; Y is beyond scope but a valid direction for future research" closes a question you cannot answer.
- Never contradict a teammate in front of the panel.

**If the panel challenges your synthetic data:**
> "Synthetic data generation from published aggregate statistics is a standard approach in restricted-microdata social science contexts, used by the World Bank, IMF, and UNDP. Every probability distribution in our generator is anchored to a published FinScope 2022 statistic. We validate the calibration quantitatively and report the discrepancies transparently. No real individuals' data is used, and no privacy risk is created."

---

*Group 2 — KYC Financial Exclusion in Zimbabwe — MSU Honours 2026*
*Knowledge Keche (R162841Q) · Lennie G. Dube (R247540M) · Jonah T. Chigaba (R2410297J)*
*Supervisor: Bridget Munyoro*
