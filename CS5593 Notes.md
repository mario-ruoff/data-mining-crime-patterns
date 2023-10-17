# CS5593 Notes

## 16 October 2023
### Rule Generation
- Start on Ch. 6 / Slide 48
- Need to review *anti-monotone* property from last Wednesday

### Compact Representation of Frequent Itemsets and Alternative Algorithm for Generating Frequent Itemsets

#### Maximal Frequent Itemsets

> **Theorem:** *If a rule X-> {Y-X} does not satisfy the confidence threshold, the any rule X' -> Y-X', where X' is a subset of X, must not satisfy the confidence threshold as well.*

This allows us to utilize the apriori principle, and be able to eliminate a lot of potential rules since they won't have a min confidence threshold as well.

> **Maximal Frequent Itemset**: An itemset is **maximal** frequent if it is frequent and **none** of its immediate **supersets** are frequent.

In a itemset cluster diagram, the itemsets **below** a particular itemset are the supersets.

All frequent itemsets an be derived from the maximal frequent itemsets, but MFIs do not contain the support of their subsets => an additional pass over the data is needed to determine support counts of subsets.

> **Closed Itemset**: an itemset is **CLOSED** if non of its **immedate supersets** has the **same support count** as the itemset.

####  FP-Growth Algorithm
*Frequent Pattern Growth*

Alternative algorithm to mine frequent itemsets that uses a compressed representation of the database using an **FP-tree**.

Once an FP-tree has been constructed, use a recursive divide-and-conquer approact to mine.

### Evaluation of Association Patterns