# 🎓 Student Satisfaction Survey Analysis and Insights

This project analyzes student satisfaction data from a survey to identify key areas of success (highest ratings) and critical areas for improvement (lowest ratings and negative sentiment). The analysis combines quantitative rating statistics with Natural Language Processing (NLP) for qualitative feedback assessment.

***

## 1. Project Overview & Objectives

The primary goal of this analysis is to provide actionable recommendations to academic administrators based on student feedback captured across multiple survey questions and optional comment fields.

### Key Objectives:
1.  **Quantitative Rating Analysis:** Process raw ratings (`Average/Percentage`) to identify top-performing and underperforming questions.
2.  **Qualitative Sentiment Analysis (NLP):** Apply **VADER (Valence Aware Dictionary and sEntiment Reasoner)** to categorize student comments as Positive, Negative, or Neutral.
3.  **Visualization:** Generate clear charts to represent satisfaction scores and sentiment distribution.
4.  **Actionable Recommendations:** Provide specific, data-driven strategies based on the lowest-rated survey items.

***

## 2. Data Processing and Cleaning

The raw data was processed within the Jupyter Notebook to prepare it for analysis and modeling.

### 2.1. Data Loading and Preparation
* The data was loaded from an Excel file (`Student_Satisfaction_Survey.csv.xlsx`).
* **Column Cleaning:** Leading/trailing spaces were stripped from column names to prevent `KeyError` during processing.

### 2.2. Feature Engineering
The combined `Average/Percentage` column was split and processed to create a usable numerical metric:

* **Average_Rating:** Extracted the numerical average score (on a 1-5 scale) from the combined text field. This is the primary metric for quantitative analysis.
* **Comments Placeholder:** Since the actual free-text comments were not available in the provided structure, placeholder comments were created and repeated (`np.tile`) across all 580 rows to enable the demonstration of the NLP pipeline.

***

## 3. Quantitative Rating Analysis

This section identifies the performance extremes using the calculated `Average_Rating`.

### ✅ Top 3 Questions with Highest Satisfaction:
The model identified factors with the highest positive student perception:

* **Rating: 5.00** | Question: Your mentor does a necessary follow-up with an assigned task...
* **Rating: 5.00** | Question: The teachers illustrate the concepts through examples and ap...
* **Rating: 5.00** | Question: How well were the teachers able to communicate?

### ❌ Top 3 Questions Indicating Areas for Improvement:
These represent the most critical issues needing immediate attention:

* **Rating: 1.33** | **Issue:** The teachers identify your strengths and encourage you to pr...
* **Rating: 1.33** | **Issue:** The teaching and mentoring process in your institution facil...
* **Rating: 1.67** | **Issue:** The teachers illustrate the concepts through examples and ap...

***

## 4. Qualitative Sentiment Analysis (NLP)

VADER Sentiment Analysis was applied to categorize the placeholder comments, providing a qualitative view of student feedback.

### Sentiment Distribution Summary:

| Sentiment Category | Proportion |
| :--- | :--- |
| **Positive** | 80.0% |
| **Neutral** | 20.0% |

### Visualization:
A **Pie Chart** clearly displays the high volume of positive feedback compared to neutral and the absence of negative sentiment in the placeholder data.

| Pie Chart |
| :---: |
|  |

***

## 5. Key Recommendations for Administrators

Recommendations are based directly on the two lowest average-rated questions:

### Recommendation 1 (Addressing Lowest Rating: 1.33)
> ⭐ **Issue:** The teachers identify your strengths and encourage you to provide the proper level of challenges.
>
> **Strategy:** Develop a mentorship program focused on **personalized student growth**. Train faculty to recognize individual student strengths and tailor assignments/challenges to provide suitable levels of academic difficulty and encouragement.

### Recommendation 2 (Addressing Second Lowest Rating: 1.33)
> ⭐ **Issue:** The teaching and mentoring process in your institution facilitates you in cognitive, social and emotional growth.
>
> **Strategy:** Host faculty development workshops focusing on **modern, interactive teaching methodologies** to improve the overall student experience and engagement, thereby facilitating holistic cognitive and social growth.

***

## 6. Repository Structure
You want to integrate the file structure into the `README.md` you were previously working on.

Here is the section of the `README.md` that displays the file structure and tools used, provided in the clean markdown format you requested:

-----

## 5\. Repository Structure and Tools Used

This project uses Python for complex data manipulation and VADER for sentiment analysis, with the final results documented directly within the Jupyter Notebook.

| Component | Primary Tool | Purpose in Project |
| :--- | :--- | :--- |
| **Data Cleaning** | **Python (Pandas)** | Conducted cleaning, processed raw rating strings, and engineered the `Average_Rating` column. |
| **Sentiment Analysis** | **Python (VADER)** | Applied NLP to qualitative comments to categorize feedback as Positive, Negative, or Neutral. |
| **Visualization** | **Python (Matplotlib/Seaborn)** | Created charts (Bar Plot, Pie Chart) to visualize ratings distribution and sentiment summary. |
| **Recommendations** | **Quantitative/Qualitative** | Derived actionable strategies from the top/bottom 3 rated questions. |

### Repository Files:

```
.
├── Task-3.ipynb                   # Primary Jupyter Notebook with all code, analysis steps, and visualizations
├── Student_Satisfaction_Survey.csv.xlsx # Original Data Source file
└── README.md                      # This documentation file
```
hi...this is bhumi