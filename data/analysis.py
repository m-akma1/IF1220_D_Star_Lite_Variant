import pandas as pd
import matplotlib.pyplot as plt
import argparse


def load_data(path):
    return pd.read_csv(path)


def aggregate(df):
    # Compute capture rate, mean cost, mean planning time per (lambda, r)
    grouped = df.groupby(['lambda','r'])
    summary = grouped.agg(
        capture_rate=('caught','mean'),
        reached_rate=('reached', 'mean'),
        mean_cost=('path_cost','mean'),
        mean_plan_time=('avg_plan_time','mean'),
        trials=('map','nunique')
    ).reset_index()
    return summary


def plot_capture_rate(summary, out_file=None):
    pivot = summary.pivot(index='r', columns='lambda', values='capture_rate')
    pivot.plot(marker='o')
    plt.title('Capture Rate over Risk Radius')
    plt.xlabel('Risk Radius (r)')
    plt.ylabel('Capture Rate')
    plt.legend(title='Lambda')
    plt.grid(True)
    if out_file:
        plt.savefig(out_file)
    else:
        plt.show()
    plt.clf()

def plot_reached_rate(summary, out_file=None):
    pivot = summary.pivot(index='r', columns='lambda', values='reached_rate')
    pivot.plot(marker='o')
    plt.title('Success Rate over Risk Radius')
    plt.xlabel('Risk Radius (r)')
    plt.ylabel('Success Rate')
    plt.legend(title='Lambda')
    plt.grid(True)
    if out_file:
        plt.savefig(out_file)
    else:
        plt.show()
    plt.clf()

def plot_mean_cost(summary, out_file=None):
    for lam in summary['lambda'].unique():
        grp = summary[summary['lambda']==lam]
        plt.plot(grp['r'], grp['mean_cost'], marker='o', label=f'λ={lam}')
    plt.title('Mean Path Cost over Risk Radius')
    plt.xlabel('Risk Radius (r)')
    plt.ylabel('Mean Path Cost')
    plt.legend()
    plt.grid(True)
    if out_file:
        plt.savefig(out_file)
    else:
        plt.show()
    plt.clf()

def plot_mean_comp_time(summary, out_file=None):
    for lam in summary['lambda'].unique():
        grp = summary[summary['lambda']==lam]
        plt.plot(grp['r'], grp['mean_plan_time'], marker='o', label=f'λ={lam}')
    plt.title('Average Plan Time over Risk Radius')
    plt.xlabel('Risk Radius (r)')
    plt.ylabel('Plan Time (in milliseconds)')
    plt.ylim(0, 1)  # Set y-axis scaling from 0 to 1
    plt.legend()
    plt.grid(True)
    if out_file:
        plt.savefig(out_file)
    else:
        plt.show()
    plt.clf()

def print_mean_plan_time_stats(summary):
    desc = summary['mean_plan_time'].describe()
    print("Descriptive statistics for mean_plan_time:")
    print(desc)

def save_summary(summary, out_path):
    summary.to_csv(out_path, index=False)


def main():
    parser = argparse.ArgumentParser(description='Analyze experiment results')
    parser.add_argument('--input', default='experiment_results.csv' , help='Path to experiment_results.csv')
    parser.add_argument('--summary', default='summary.csv', help='Output summary CSV')
    parser.add_argument('--plot-capture', default='capture_rate.png', help='Output capture rate plot')
    parser.add_argument('--plot-reached', default='reached_rate.png', help='Output reached rate plot')
    parser.add_argument('--plot-cost', default='mean_cost.png', help='Output mean cost plot')
    parser.add_argument('--plot-compute', default='plan_time.png', help='Output mean computation plan time plot')
    args = parser.parse_args()

    df = load_data(args.input)
    summary = aggregate(df)
    save_summary(summary, args.summary)
    plot_capture_rate(summary, args.plot_capture)
    plot_reached_rate(summary, args.plot_reached)
    plot_mean_cost(summary, args.plot_cost)
    plot_mean_comp_time(summary, args.plot_compute)
    print_mean_plan_time_stats(summary)

if __name__ == '__main__':
    main()
