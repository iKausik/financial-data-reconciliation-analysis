from query_executor import get_reconciled_txns, get_unmatched_from_bank_txns, get_unmatched_from_ledger_txns, get_total_by_currency
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

# Get the data
reconciled = get_reconciled_txns()
unmatched_bank = get_unmatched_from_bank_txns()
unmatched_ledger = get_unmatched_from_ledger_txns()
total_by_currency = get_total_by_currency()

# Set the style and color palette for all plots
sns.set_style("whitegrid")  # Changed from plt.style.use('seaborn')

# Modern fintech color palette
colors = ["#003f5c", "#bc5090", "#ff6361", "#ffa600", "#58508d"]
# colors = ["#63993D", "#0f62fe", "#ffa600", "#ff6361", "#8a3ffc"] # best suited for multi-line charts

# Monochrome color palette for Charts
# colors = ["#2E5077", "#537A9F", "#91AEC4", "#304D63", "#8B9BA3"] # grey shades
# colors= ["#0f62fe", "#4589ff", "#78a9ff", "#a6c8ff", "#d0e2ff"] # blue shades
# colors = ["#8a3ffc", "#a56eff", "#be95ff", "#d4bbff", "#e8daff"] # purple shades
# colors = ["#9E4A06", "#ffbb78", "#ffddc1", "#f7b2a3", "#f5c6cb"] # orange shades
# colors = ["#63993D", "#87BB62", "#A8D8B9", "#C4E1D5", "#E0F2E9"] # green shades
# colors = ["#007d79", "#009d9a", "#08bdba", "#3ddbd9", "#9ef0f0"] # teal shades
# colors = ["#da1e28", "#fa4d56", "#ff8389", "#ffb3b8", "#ffd7d9"] # red shades

sns.set_palette(colors)

def plot_transaction_distribution():
    """
    1. Bar chart showing matched vs unmatched transactions
    """
    print(len(reconciled))
    print(len(unmatched_bank))
    print(len(unmatched_ledger))
    plt.figure(figsize=(12, 6))
    
    # Prepare data
    data = {
        'Status': ['Reconciled', 'Unmatched Bank', 'Unmatched Ledger'],
        'Count': [len(reconciled), len(unmatched_bank), len(unmatched_ledger)]
    }

    # Create bar plot with enhanced style
    ax = sns.barplot(
        data=data,
        x='Status',
        y='Count',
        hue='Status',
        palette=colors[:3],
        width=0.7,
        alpha=0.9
    )
    
    # Enhanced customization
    plt.title('Transaction Distribution', 
              fontsize=16, 
              pad=20,
              fontweight='bold')
    plt.xlabel('Status', fontsize=12, fontweight='bold')
    plt.ylabel('Number of Transactions', fontsize=12, fontweight='bold')
    
    # Add value labels on bars with enhanced style
    for i in ax.containers:
        ax.bar_label(i, fmt='%d', padding=3, fontsize=11, fontweight='bold')
    
    # Enhance grid and spines
    ax.grid(axis='y', linestyle='--', alpha=0.7)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_linewidth(1.5)
    ax.spines['bottom'].set_linewidth(1.5)
    
    # Adjust tick parameters
    plt.xticks(fontsize=11)
    plt.yticks(fontsize=11)
    
    # Add subtle background color
    ax.set_facecolor('#f8f9fa')
    plt.gcf().set_facecolor('#ffffff')
    
    plt.tight_layout()
    plt.show()
    # plt.savefig('../reports/figures/transaction_distribution.png', dpi=300, bbox_inches='tight')
    plt.close()

def plot_mismatch_analysis():
    """
    2. Stacked bar chart showing timing vs amount mismatches
    """
    plt.figure(figsize=(12, 6))
    
    # Prepare data
    reconciled['date_mismatch'] = reconciled['bank_txn_date'] != reconciled['internal_txn_date']
    reconciled['amount_mismatch'] = reconciled['bank_txn_amount'] != reconciled['internal_txn_amount']
    
    mismatch_data = pd.DataFrame({
        'Date Mismatch': [sum(reconciled['date_mismatch']), sum(~reconciled['date_mismatch'])],
        'Amount Mismatch': [sum(reconciled['amount_mismatch']), sum(~reconciled['amount_mismatch'])]
    }, index=['Mismatch', 'Match'])
    
    # Create stacked bar plot
    ax = mismatch_data.plot(
        kind='bar',
        stacked=True,
        figsize=(12, 6),
        width=0.7,
        color=colors[1:3],
        alpha=0.9
    )
    
    # Enhanced customization
    plt.title('Transaction Mismatch Analysis', 
              fontsize=16, 
              pad=20,
              fontweight='bold')
    plt.xlabel('Mismatch Type', fontsize=12, fontweight='bold')
    plt.ylabel('Number of Transactions', fontsize=12, fontweight='bold')
    plt.legend(title='Status', fontsize=11, labels=['Date Count', 'Amount Count'])
    
    # Add value labels with enhanced style
    for c in ax.containers:
        ax.bar_label(c, fmt='%d', label_type='center', fontsize=11, fontweight='bold')
    
    # Enhance grid and spines
    ax.grid(axis='y', linestyle='--', alpha=0.7)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_linewidth(1.5)
    ax.spines['bottom'].set_linewidth(1.5)
    
    # Adjust tick parameters
    plt.xticks(fontsize=11, rotation=0)
    plt.yticks(fontsize=11)
    
    # Add subtle background color
    ax.set_facecolor('#f8f9fa')
    plt.gcf().set_facecolor('#ffffff')
    
    plt.tight_layout()
    plt.show()
    # plt.savefig('../reports/figures/mismatch_analysis.png', dpi=300, bbox_inches='tight')
    plt.close()

def plot_currency_comparison():
    """
    Plot currency-wise comparison of bank vs internal amounts
    """
    plt.figure(figsize=(12, 6))
    
    # Melt the dataframe for seaborn
    melted_data = pd.melt(
        total_by_currency,
        id_vars=['currency'],
        value_vars=['total_bank_amount', 'total_internal_amount'], 
        var_name='Source',
        value_name='Amount'
    )
    
    # Clean up the source names for legend
    melted_data['Source'] = melted_data['Source'].map({
        'total_bank_amount': 'Bank Amount',
        'total_internal_amount': 'Internal Amount'
    })
    
    # Create grouped bar plot
    ax = sns.barplot(
        data=melted_data,
        x='currency',
        y='Amount',
        hue='Source',
        palette=colors[1:3],
        alpha=0.9
    )
    
    # Enhanced customization
    plt.title('Bank vs Internal Amounts by Currency', 
              fontsize=16, 
              pad=20,
              fontweight='bold')
    plt.xlabel('Currency', fontsize=12, fontweight='bold')
    plt.ylabel('Amount', fontsize=12, fontweight='bold')
    plt.legend(fontsize=11)
    
    # Add value labels with enhanced style
    for container in ax.containers:
        ax.bar_label(container, fmt='%.2f', padding=3, rotation=0, fontsize=11, fontweight='bold')
    
    # Enhance grid and spines
    ax.grid(axis='y', linestyle='--', alpha=0.7)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_linewidth(1.5)
    ax.spines['bottom'].set_linewidth(1.5)
    
    # Adjust tick parameters
    plt.xticks(fontsize=11)
    plt.yticks(fontsize=11)
    
    # Add subtle background color
    ax.set_facecolor('#f8f9fa')
    plt.gcf().set_facecolor('#ffffff')
    
    plt.tight_layout()
    plt.show()
    # plt.savefig('../reports/figures/currency_comparison.png', dpi=300, bbox_inches='tight')
    plt.close()

def plot_transaction_trend():
    """
    Plot trend line chart showing transactions over time
    """
    plt.figure(figsize=(12, 6))
    
    # Prepare data
    reconciled_by_date = reconciled.groupby('bank_txn_date').size().reset_index(name='count')
    unmatched_bank_by_date = unmatched_bank.groupby('txn_date').size().reset_index(name='count')
    unmatched_ledger_by_date = unmatched_ledger.groupby('txn_date').size().reset_index(name='count')
    
    # Create line plot
    plt.plot(reconciled_by_date['bank_txn_date'], reconciled_by_date['count'], 
             label='Reconciled', linewidth=2, marker='o', markersize=4)
    plt.plot(unmatched_bank_by_date['txn_date'], unmatched_bank_by_date['count'],
             label='Unmatched Bank', linewidth=2, marker='o', markersize=4)
    plt.plot(unmatched_ledger_by_date['txn_date'], unmatched_ledger_by_date['count'],
             label='Unmatched Ledger', linewidth=2, marker='o', markersize=4)
    
    # Enhanced customization
    plt.title('Transaction Trends Over Time',
              fontsize=16,
              pad=20,
              fontweight='bold')
    plt.xlabel('Date', fontsize=12, fontweight='bold')
    plt.ylabel('Number of Transactions', fontsize=12, fontweight='bold')
    plt.legend(fontsize=11)
    
    # Enhance grid and spines
    ax = plt.gca()
    ax.grid(linestyle='--', alpha=0.7)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_linewidth(1.5)
    ax.spines['bottom'].set_linewidth(1.5)
    
    # Adjust tick parameters
    plt.xticks(fontsize=11, rotation=45)
    plt.yticks(fontsize=11)
    
    # Add subtle background color
    ax.set_facecolor('#f8f9fa')
    plt.gcf().set_facecolor('#ffffff')
    
    plt.tight_layout()
    plt.show()
    # plt.savefig('../reports/figures/transaction_trends.png', dpi=300, bbox_inches='tight')
    plt.close()

def generate_summary_report():
    """
    Generate a text summary of the analysis based on the four visualization charts
    """
    print("\nReconciliation Analysis Summary")
    print("=" * 50)
    
    # Transaction Distribution Summary (from plot_transaction_distribution)
    total_txns = len(reconciled) + len(unmatched_bank) + len(unmatched_ledger)
    print(f"Total Transactions: {total_txns:,}")
    print(f"Reconciled: {len(reconciled):,} ({len(reconciled)/total_txns*100:.1f}%)")
    print(f"Unmatched Bank: {len(unmatched_bank):,} ({len(unmatched_bank)/total_txns*100:.1f}%)")
    print(f"Unmatched Ledger: {len(unmatched_ledger):,} ({len(unmatched_ledger)/total_txns*100:.1f}%)")
    
    # Mismatch Analysis Summary (from plot_mismatch_analysis)
    date_mismatches = reconciled['bank_txn_date'] != reconciled['internal_txn_date']
    amount_mismatches = reconciled['bank_txn_amount'] != reconciled['internal_txn_amount']
    print(f"\nMismatch Analysis:")
    print(f"Date Mismatches: {sum(date_mismatches):,} ({sum(date_mismatches)/len(reconciled)*100:.1f}% of reconciled)")
    print(f"Amount Mismatches: {sum(amount_mismatches):,} ({sum(amount_mismatches)/len(reconciled)*100:.1f}% of reconciled)")
    
    # Currency Comparison Summary (from plot_currency_comparison)
    print("\nCurrency-wise Comparison:")
    for _, row in total_by_currency.iterrows():
        diff = abs(row['total_bank_amount'] - row['total_internal_amount'])
        print(f"{row['currency']}: Bank={row['total_bank_amount']:,.2f}, Internal={row['total_internal_amount']:,.2f}")
        print(f"Difference: {diff:,.2f}")
    
    # Transaction Trend Summary (from plot_transaction_trend)
    print("\nTransaction Trends:")
    reconciled_by_date = reconciled.groupby('bank_txn_date').size()
    peak_date = reconciled_by_date.idxmax()
    min_date = reconciled_by_date.idxmin()
    print(f"Peak reconciled transactions: {reconciled_by_date.max():,} on {peak_date.strftime('%Y-%m-%d')}")
    print(f"Lowest reconciled transactions: {reconciled_by_date.min():,} on {min_date.strftime('%Y-%m-%d')}")
    print(f"Average daily reconciled transactions: {reconciled_by_date.mean():.1f}")
    print(f"Total days analyzed: {len(reconciled_by_date):,}")
    print(f"Date range: {reconciled_by_date.index.min().strftime('%Y-%m-%d')} to {reconciled_by_date.index.max().strftime('%Y-%m-%d')}")

def generate_all_reports():
    """
    Generate all visualizations and summary report
    """
    try:
        # Generate visualizations
        plot_transaction_distribution()
        plot_mismatch_analysis()
        plot_currency_comparison()
        plot_transaction_trend()
        print("Visualizations generated successfully!")

        # Generate summary report
        generate_summary_report()
        print("\nAll reports generated successfully!")
        
    except Exception as e:
        print(f"Error generating reports: {str(e)}")

if __name__ == "__main__":
    try:
        generate_all_reports()
    except Exception as e:
        print(f"Error in main execution: {str(e)}")
