from datetime import date

today = date.today()
print(today)




# import pandas as pd
# import numpy as np

# # Create a sample DataFrame with 10 columns including 'STATUS'
# np.random.seed(0)  # For reproducibility

# # Possible statuses
# statuses = ['OPEN', 'CLOSED', 'PENDING', 'CANCELLED']

# # Create data
# data = {
#     f'Column_{i}': np.random.randint(1, 100, 20) for i in range(8)
# }
# data['Priority'] = np.random.randint(1, 5, 20)  # Priority from 1 (low) to 4 (high)
# data['STATUS'] = np.random.choice(statuses, size=20)

# # Create the DataFrame
# df = pd.DataFrame(data)

# print("Original DataFrame:")
# print(df)

# # Define the desired order of statuses
# status_order = ['OPEN', 'PENDING', 'CANCELLED', 'CLOSED']

# # Filter and sort by STATUS and Priority (descending)
# filtered_df = df[df['STATUS'].isin(status_order)].copy()
# filtered_df['STATUS'] = pd.Categorical(filtered_df['STATUS'], categories=status_order, ordered=True)
# filtered_df = filtered_df.sort_values(['STATUS', 'Priority'], ascending=[True, False]).reset_index(drop=True)

# print("\nFiltered and Ordered DataFrame (by STATUS and descending Priority):")
# print(filtered_df)
