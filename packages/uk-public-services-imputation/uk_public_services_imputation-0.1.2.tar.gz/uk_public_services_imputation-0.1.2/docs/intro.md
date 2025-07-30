# Public services in PolicyEngine UK

This report sets out the methodology we've developed to incorporate the value of public services in PolicyEngine's UK tax and benefit model. By integrating both machine learning techniques and administrative data, we can now model the distributional impacts of spending on services like education and healthcare – not just cash transfers. This represents a significant advance in our ability to assess how government policy affects living standards across the income distribution.

## Why this matters

Tax and benefit microsimulation models typically focus on cash – the direct taxes people pay and the benefits they receive. But around half of what government does for households comes in the form of public services like education, healthcare and social care. 

These 'benefits in kind' are hugely important for living standards but are often neglected in distributional analysis. A full assessment of how government policy affects different households needs to take into account both cash and services.

## Our approach

We've used two complementary methods to incorporate public services in the PolicyEngine UK model: 

### Impute existing government imputations from the ETB

Our primary approach leverages the existing methodology used by the government itself. The Office for National Statistics already produces estimates of the value of public services to households in their Effects of Taxes and Benefits (ETB) dataset.

To incorporate these values into our model – which uses the Family Resources Survey (FRS) – we employ a quantile regression forest model. This machine learning approach allows us to:

* Identify patterns in how public service values are distributed across different types of households in the ETB data
* Apply these patterns to predict what households with similar characteristics in our FRS dataset would receive
* Maintain consistency with the government's own distributional analysis at fiscal events

The model considers factors including household composition, age, income, employment status, disability status and benefit receipt. It produces household-level estimates for the value of education, healthcare, travel subsidies and other public services.

By using the government's own imputation approach – rather than developing an entirely new methodology – we ensure our analysis is comparable with HM Treasury's distributional analysis at Budget and Spending Review events.

### Impute NHS usage from administrative data

For healthcare specifically, we've implemented an improved approach based on recent work by the Resolution Foundation in their 'At Your Service' report. Rather than relying solely on survey data, this method uses administrative data from NHS Digital on healthcare utilisation and costs by age and sex.

The approach works as follows:

* We use NHS Digital data on the number and cost of A&E visits, outpatient appointments and inpatient admissions by age band and sex
* For each individual in our FRS dataset, we assign the average service utilisation and cost associated with their demographic group
* We aggregate these values to the household level to calculate the total in-kind benefit from NHS spending

This method provides a more direct link between actual healthcare usage patterns and our estimates, without requiring complex survey-based imputations.

## Limitations and future improvements

These methods enable PolicyEngine's microsimulation model to incorporate the value of (changes to) public service spending. But there are some limitations:

* The approaches focus largely on expenditure, not quality or outcomes
* Geographic variations in service quality and cost are not fully captured
* The imputation introduces an additional layer of uncertainty compared to direct measurement
* Behavioural responses to policy changes are not modelled

## Conclusion

By incorporating the value of public services in PolicyEngine UK, we can now provide a more complete picture of how government policy affects household living standards. This development enables policymakers, researchers and the public to better understand the full distributional impacts of fiscal choices – from tax and benefit reforms to changes in departmental spending.
