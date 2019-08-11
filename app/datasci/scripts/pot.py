# Import necessary libraries
import matplotlib.pyplot as plt
import seaborn as sns

# Reset default params
sns.set()

# Set context to `"paper"`
sns.set_context("paper")

print("xxx")
# Load iris data
iris = sns.load_dataset("iris")

# Construct iris plot
sns.swarmplot(x="species", y="petal_length", data=iris)

# Show plot
print_figure(plt)