import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.cluster.hierarchy import linkage

class MODEL_FEAT_TRACK:
    def __init__(self,heros):
        self.ft_scores = np.array([[0.0]*heros.env.num_feat for i in range(heros.env.num_instances)]) #feature tracking score array
        self.model_index = None


    def get_correct_set_scores(self,heros):
        """ Generate a feature score list based on the correct set of the current instance"""
        correct_score_list = np.array([0.0]*heros.env.num_feat)
        correct_rule_count = 0
        for rule_index in heros.model_population.correct_set:
            correct_rule_count += heros.model_population.target_rule_set[rule_index].numerosity
            specificity = len(heros.model_population.target_rule_set[rule_index].condition_indexes)
            for feat in heros.model_population.target_rule_set[rule_index].condition_indexes:
                correct_score_list[feat] += heros.model_population.target_rule_set[rule_index].useful_accuracy
        return correct_score_list, correct_rule_count
    

    def batch_calculate_ft_scores(self,heros,index):
        """ Calculates feature tracking scores of all instances in the training dataset based on a fixed final rule population. """
        # Get the target rule set for feature tracking score calculation
        heros.model_population.get_target_model(index)
        self.model_index = index
        for instance_index in range(heros.env.num_instances):
            # Get current instance properties
            instance_state = heros.env.train_data[0][instance_index]
            outcome_state = heros.env.train_data[1][instance_index]
            # Make {M}
            heros.model_population.make_eval_match_set(instance_state,heros)
            # Make {C}
            heros.model_population.make_eval_correct_set(outcome_state,heros)
            # Make correct set score lists
            correct_score_list, correct_rule_count = self.get_correct_set_scores(heros)
            # Set feature tracking scores for this instance
            for feat in range(heros.env.num_feat):
                self.ft_scores[instance_index][feat] += correct_score_list[feat]
            heros.model_population.clear_sets()


    def export_ft_scores(self,heros,feature_names):
        """ Prepares and exports a dataframe capturing the feature tracking scores."""
        #columns = list(range(heros.env.num_feat))
        ft_df = pd.DataFrame(self.ft_scores, columns=feature_names)
        ft_df['row_id'] = heros.env.instance_ids
        return ft_df 
    
    
    def plot_clustered_ft_heatmap(self, ft_df, feature_names, specified_filter, show=True, save=False, output_path=None):
        """ Generates a clustered heatmap of feature tracking scores. Scores values are scaled within rows between 0 and 1 for 
            hierarchical clustering between both rows and columns to determine clustering arrangment in plot. Scores values are 
            globally scaled (min/max out of all feature tracking scores) for displaying heatmap values on plot. 
            This makes clustering based on relative ft scores within an instance, while preserving relative feature tracking
            scores between individual instances to better identify instances with lower overall tracking scores.
        """
        # Prepare dataframe
        ft_df.columns = feature_names #Add original feature names back to columns rather than indexes
        #Filter out any feature columns with all zero values
        if specified_filter != None and specified_filter != 'None':
            cols_to_keep = (ft_df != 0.0).sum(axis=0) >= specified_filter
            ft_df = ft_df.loc[:, cols_to_keep]

        #ft_df = ft_df.loc[:, (ft_df != 0).any(axis=0)]
        # Scale feature tracking scores
        df_min = ft_df.min().min()
        df_max = ft_df.max().max()
        ft_df_all_scaled = (ft_df - df_min) / (df_max - df_min)

        #ft_df_row_scaled = ft_df.apply(lambda x: (x - x.min()) / (x.max() - x.min()) if x.max() != x.min() else np.zeros_like(x), axis=1) # Scale within rows individually

        # Perform hierarchical clustering on columns
        col_linkage = linkage(ft_df_all_scaled.T, method='average', metric='euclidean', optimal_ordering=True)
        # Perform hierarchical clustering on rows
        row_linkage = linkage(ft_df_all_scaled, method='average', metric='euclidean', optimal_ordering=True)
        # Create a seaborn clustermap
        clustermap = sns.clustermap(ft_df_all_scaled, row_linkage=row_linkage, col_linkage=col_linkage, cmap='viridis', figsize=(10, 10))
        clustermap.ax_heatmap.set_xlabel('Features', fontsize=12)
        clustermap.ax_heatmap.set_ylabel('Instances', fontsize=12)
        clustermap.ax_heatmap.set_yticks([])
        # Dynamicaly update x-tick label text size based on number of features in the dataset (up to a minimum )
        num_features = ft_df_all_scaled.shape[1]
        min_text_size = 4
        max_text_size = 12
        font_size = max(min_text_size, max_text_size - num_features // min_text_size)  # Adjust font size based on the number of features
        clustermap.ax_heatmap.set_xticklabels(clustermap.ax_heatmap.get_xticklabels(), rotation=90, fontsize=font_size)
        if save:
            plt.savefig(output_path+'/clustered_rule_set_'+str(self.model_index)+'_ft_heatmap.png', bbox_inches="tight")

        if show:
            plt.show()
