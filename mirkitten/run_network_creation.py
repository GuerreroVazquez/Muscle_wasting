### This will be the main script to run the network creation
# It will take the arguments from the command line and run the network creation
# It will also check that the arguments are correct
# It will print the path where the network was saved

# add to the path mirkitten
import sys
import os.path

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
os.chdir(BASE_DIR)
pwd = os.getcwd()
print(pwd)
import argparse
import create_network as cn
import logging
# Set up logging to mitkitten.log
logging.basicConfig(filename='mirkitten.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


if __name__ == '__main__':

    # The function needs dds_files_path, only_DE=False, threshold=None, pvalue=0.05, interest='stat', species='human', save_name='tf_network.csv'

    parser = argparse.ArgumentParser(description="Run the network creation")
    parser.add_argument('--dds_files', type=str,
                        help='YAML file with the names of the comparisons and the path to the DDS file')
    parser.add_argument('--only_DE', type=bool, help='If only DE genes are going to be used', default=False)
    parser.add_argument('--threshold', type=float, help="pvalue to determine when a pathwway is enriched.",
                        default=None)
    parser.add_argument('--pvalue', type=float, help="pvalue to determine when a pathway is significantly enrriched.",
                        default=0.05)
    parser.add_argument('--interest', type=str,
                        help="What is going to be the base of desicion. log2FoldChange or stat.", default='stat')
    parser.add_argument('--save_name', type=str, help='Path to save the results', default='tf_network.csv')

    args = parser.parse_args()
    if args.pvalue <= 0 or args.pvalue > 1:
        raise ValueError('Pvalue must be >0 and <=1')
    if args.threshold and args.threshold < 0:
        raise ValueError('Threshold must be >=0')
    if args.interest not in ['stat', 'log2FoldChange']:
        raise ValueError('Interest must be in ["stat", "log2FoldChange"]')

    logging.info(f'Running network creation with dds_files: {args.dds_files}, only_DE: {args.only_DE}, \
                 threshold: {args.threshold}, pvalue: {args.pvalue}, interest: {args.interest}, save_name: {args.save_name}')
    network = cn.new_network(args.dds_files, only_DE=args.only_DE, threshold=args.threshold, pvalue=args.pvalue,
                             interest=args.interest, save_name=args.save_name)
    network.collect_genes()
    network.get_network()
    network.generate_cytoscape_json()
    network.save_network()
    print('Network saved in {}'.format(args.save_name))
