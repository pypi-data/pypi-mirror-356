import copy
import math
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter

class RULE_PARETO:
    def __init__(self):  
        #Definte the parts of the Pareto Front
        self.rule_front = []  #list of objective pair sets (useful_accuracy,useful_coverage) for each non-dominated rule (ordered by increasing accuracy)
        self.rule_front_scaled = []
        self.metric_limits = [None]*2 #assumes two metrics being optimized
        self.front_diagonal_lengths = [] # length of the diagonal lines from the orgin to each point on the pareto front (used to calculate rule fitness)


    def update_front(self,candidate_metric_1,candidate_metric_2,objectives):
        """  Handles process of checking and updating the rule pareto front. Only set up for two objectives. """
        original_front = copy.deepcopy(self.rule_front)
        candidate_rule = (candidate_metric_1,candidate_metric_2)
        if not candidate_rule in self.rule_front: # Check that candidate rule objectives are not equal to any existing objective pairs on the front
            non_dominated_rules = []
            candidate_dominated = False
            for front_rule in self.rule_front:
                if self.dominates(front_rule,candidate_rule,objectives): #does front rule dominate candidate rule (if so, this check is ended)
                    candidate_dominated = True #prevents candidate from being added 
                    break # original front is preserved
                elif not self.dominates(candidate_rule,front_rule,objectives): #does the candidate rule dominate the front rule (if so it will get added to the front)
                    non_dominated_rules.append(front_rule)
            if candidate_dominated: #at least one front rule dominates the candidate rule
                non_dominated_rules = self.rule_front
            else: #no front rules dominate the candidate rule
                non_dominated_rules.append(candidate_rule)
            # Update the rule front to include only non dominated rules
            self.rule_front = sorted(non_dominated_rules, key=lambda x: x[0])
            # Update the maximum values found in rules on the pareto front and update rule_front_scaled as needed
            self.metric_limits[0] = max(self.rule_front, key=lambda x: x[0])[0]
            self.metric_limits[1] = max(self.rule_front, key=lambda x: x[1])[1]
            if self.metric_limits[1] != 0.0:
                self.rule_front_scaled = [(x[0],x[1] /float(self.metric_limits[1])) for x in self.rule_front]
            else:
                self.rule_front_scaled = self.rule_front
        if original_front == self.rule_front:
            return False
        else:
            return True


    def dominates(self,p,q,objectives):
        """Check if p dominates q. A rule dominates another if it has a more optimal value for at least one objective."""
        better_in_all_objectives = True
        better_in_at_least_one_objective = False
        for val1, val2, obj in zip(p, q, objectives):
            if obj == 'max':
                if val1 < val2:
                    better_in_all_objectives = False
                if val1 > val2:
                    better_in_at_least_one_objective = True
            elif obj == 'min':
                if val1 > val2:
                    better_in_all_objectives = False
                if val1 < val2:
                    better_in_at_least_one_objective = True
            else:
                raise ValueError("Objectives must be 'max' or 'min'")
        return better_in_all_objectives and better_in_at_least_one_objective


    def get_pareto_fitness(self,candidate_metric_1,candidate_metric_2, landscape,heros):
        """ Calculate rule fitness releative to the rule pareto front. Only set up for two objectives. """
        front_penalty_scalar = 0.99
        ### SPECIAL CASE HANDLING -------------------------------------------------------------------------------------------------------------------------------------------
        ## Special Case 1: EMPTY FRONT - Only one point on front, both with zero values (i.e. no front exists) (unlikely special case if working on data with no/very low signal)
        if len(self.rule_front_scaled) == 1 and self.rule_front_scaled[0][0] == 0.0 and self.rule_front_scaled[0][1] == 0.0:
            return None
        ## PARETO LANDSCAPE PLOTTING Special Cases: Handles special cases when calculating fitness landscape for visualization---------
        if landscape: 
            ## Special Case 2: BEYOND DOTTED LINES - Point is beyond one of the Pareto front edges (denoted by dotted line on viz)(return max fitness for viz)
            if candidate_metric_1 > 1.0 or candidate_metric_2 / float(self.metric_limits[1]) > 1.0:
                return 1.0
            ## Special Case 3: BEYOND REST OF FRONT - Front contains more than one solution and point is beyond front but not greater than either front edge (i.e. the optimal corner of the pareto front) (return max fitness for viz)
            if candidate_metric_1 > self.rule_front_scaled[0][0] and candidate_metric_2 / float(self.metric_limits[1]) > self.rule_front_scaled[-1][1] and self.point_beyond_front(candidate_metric_1,candidate_metric_2 / float(self.metric_limits[1])):
                return 1.0 
        #------------------------------------------------------------------------------------------------------------------------------
        ## Special Case 4: ZERO FITNESS - Point is at minimum fitness point (i.e. both target metrics minimized - least optimal)
        if candidate_metric_1 == 0.0 and candidate_metric_2 == 0.0:
            return 0.0
        ## Special Case 5: POINT ON FRONT - Point is on the front (returns optimal fitness when nu=1, and slightly penalized fitness for less accurate front points when nu>1)
        elif (candidate_metric_1,candidate_metric_2) in self.rule_front: # Rules on the front return an ideal fitness
            if heros.nu > 1: # Apply pressure to maximize model accuracy 
                if candidate_metric_1 == self.metric_limits[0]:
                    return 1.0
                else:
                    fitness_adjustment = front_penalty_scalar + ((candidate_metric_1/self.metric_limits[0])*(1.0-front_penalty_scalar))
                    return fitness_adjustment * pow(candidate_metric_1 , heros.nu)
            else: 
                return 1.0
        ## Special Case 6: MAXIMUM USEFUL ACCURACY - Point has maximum metric 1 (i.e. useful accuracy) i.e. on the front edge (dotted line), but not on the front itself.
        elif candidate_metric_1 == self.metric_limits[0]:
            fitness_adjustment = front_penalty_scalar + ((candidate_metric_2/self.metric_limits[1])*(1.0-front_penalty_scalar))
            return fitness_adjustment
        
        ## Special Case 7: MAXIMUM USEFUL COVERAGE - Point has maximum metric 2 (i.e. useful coverage) i.e. on the other front edge (dotted line), but not on the front itself. 
        elif candidate_metric_2 == self.metric_limits[1]:
            fitness_adjustment = front_penalty_scalar + ((candidate_metric_1/self.metric_limits[0])*(1.0-front_penalty_scalar))
            if heros.nu > 1: # Apply pressure to maximize model accuracy 
                return fitness_adjustment * pow(candidate_metric_1 , heros.nu)
            else:
                return fitness_adjustment

        ### TYPICAL CASE HANDLING ----------------------------------------------------------------------------------------------------------------------------------------------
        ## All other points have fitness calculated based on the distance from the point to the nearest point on the pareto front (or front edge)
        else:
            scaled_candidate_metric_2 = candidate_metric_2 / float(self.metric_limits[1])
            rule_objectives = (candidate_metric_1,scaled_candidate_metric_2)
            # ADD ALL FRONT LINE SEGMENTS ----------------------------------
            # Find the closest distance between the rule and the pareto front
            temp_front = [(0.0,self.rule_front_scaled[0][1])] #max coverage boundary (First segment)
            for front_point in self.rule_front_scaled:
                temp_front.append(front_point)
            temp_front.append((self.rule_front_scaled[-1][0],0.0)) #max accuracy boundary (last segment)
            # FIND MINIMUM DISTANCE TO FRONT LINE SEGMENT -------------------
            min_distance = float('inf')
            temp_distance_list = []
            for i in range(len(temp_front) - 1):
                segment_start = temp_front[i]
                segment_end = temp_front[i + 1]
                temp_distance_list.append(self.point_to_segment_distance(rule_objectives, segment_start, segment_end))
            min_distance, min_idx = min((val, idx) for idx, val in enumerate(temp_distance_list))
            if min_idx == len(temp_distance_list) - 1: #max accuracy boundary
                fitness_adjustment = front_penalty_scalar + ((candidate_metric_2/self.metric_limits[1])*(1.0-front_penalty_scalar))
                pareto_fitness = (1 - min_distance) * fitness_adjustment
            elif min_idx == 0: # max coverage boundary
                fitness_adjustment = front_penalty_scalar + ((candidate_metric_1/self.metric_limits[0])*(1.0-front_penalty_scalar))
                pareto_fitness = (1 - min_distance) * fitness_adjustment
            else:
                pareto_fitness = 1 - min_distance #original
                if heros.nu > 1:
                    fitness_adjustment = front_penalty_scalar + ((candidate_metric_1/self.metric_limits[0])*(1.0-front_penalty_scalar))
                    pareto_fitness = pareto_fitness * fitness_adjustment
            if heros.nu > 1: # Apply pressure to maximize rule accuracy
                pareto_fitness = pareto_fitness * pow(candidate_metric_1 , heros.nu)
            return pareto_fitness
        
        
    def point_to_segment_distance(self, point, segment_start, segment_end):
        """ """
        # Vector from segment start to segment end (normalize vector so starting point is 0,0)
        segment_vector = np.array(segment_end) - np.array(segment_start)
        # Vector from segment start to the point (normalize vector so starting point is 0,0)
        point_vector = np.array(point) - np.array(segment_start)
        # Project the point_vector onto the segment_vector to find the closest point on the segment
        segment_length_squared = np.dot(segment_vector, segment_vector) #Calculate segment length squared to be used to do the projection
        if segment_length_squared == 0: #Safty check that the segment start and stop are not the same (if so just return distance to that single point)
            # The segment start and end points are the same
            return self.euclidean_distance(point, segment_start)
        # If segment has length: project the point vector onto the segment vector (identifies the perpendicular intersect)
        projection = np.dot(point_vector, segment_vector) / segment_length_squared
        projection_clamped = max(0, min(1, projection)) #checks if the interstect is within the segment (because the projection was forced between 0, and 1)
        # Find the closest point on the segment (either the perpendicular intersect or distance to segment end)
        closest_point_on_segment = np.array(segment_start) + projection_clamped * segment_vector
        # Return the distance from the point to this closest point on the segment
        return self.euclidean_distance(point, closest_point_on_segment)
    

    def euclidean_distance(self,point1,point2):
        """ Calculates the euclidean distance between two n-dimensional points"""
        if len(point1) != len(point2):
            raise ValueError("Both points must have the same number of dimensions")
        distance = math.sqrt(sum((y - x) ** 2 for y, x in zip(point1, point2)))
        return distance


    def slope(self,point1,point2):
        """ Calculates the slopes between two 2-dimensional points """
        if point1[1] == point2[1]: # line is vertical (both points have 0 coverage)
            slope = np.inf
        else:
            slope = (point2[0] - point1[0]) / (point2[1] - point1[1])
        return slope
    

    def point_beyond_front(self,candidate_metric_1,scaled_candidate_metric_2):
        """ Used for creating pareto front landscape visualization background fitness landscape. """
        # Define line segment from the origin (0,0) to the rule's objective (x,x)
        rule_start = (0,0)
        rule_end = (candidate_metric_1,scaled_candidate_metric_2)
        # Identify segments making up front to check
        intersects = False
        i = 0
        while not intersects and i < len(self.rule_front_scaled) - 1:
            segment_start = self.rule_front_scaled[i]
            segment_end = self.rule_front_scaled[i + 1]
            intersects = self.do_intersect(rule_start,rule_end,segment_start,segment_end)
            if intersects:
                return True
            i += 1
        return False
    

    def do_intersect(self,p1, q1, p2, q2):
        """ Main function to check whether the line segment p1q1 and p2q2 intersect. """
        # Find the four orientations needed for the general and special cases
        o1 = self.orientation(p1, q1, p2)
        o2 = self.orientation(p1, q1, q2)
        o3 = self.orientation(p2, q2, p1)
        o4 = self.orientation(p2, q2, q1)
        # General case
        if o1 != o2 and o3 != o4:
            return True
        # Special cases
        # p1, q1 and p2 are collinear and p2 lies on segment p1q1
        if o1 == 0 and self.on_segment(p1, p2, q1):
            return True
        # p1, q1 and q2 are collinear and q2 lies on segment p1q1
        if o2 == 0 and self.on_segment(p1, q2, q1):
            return True
        # p2, q2 and p1 are collinear and p1 lies on segment p2q2
        if o3 == 0 and self.on_segment(p2, p1, q2):
            return True
        # p2, q2 and q1 are collinear and q1 lies on segment p2q2
        if o4 == 0 and self.on_segment(p2, q1, q2):
            return True
        return False


    def on_segment(self, p, q, r):
        """
        Given three collinear points p, q, r, the function checks if point q lies on the segment pr.
        """
        if q[0] <= max(p[0], r[0]) and q[0] >= min(p[0], r[0]) and q[1] <= max(p[1], r[1]) and q[1] >= min(p[1], r[1]):
            return True
        return False


    def orientation(self, p, q, r):
        """
        To find the orientation of the ordered triplet (p, q, r).
        The function returns:
        0 -> p, q, and r are collinear
        1 -> Clockwise
        2 -> Counterclockwise
        """
        val = (q[1] - p[1]) * (r[0] - q[0]) - (q[0] - p[0]) * (r[1] - q[1])
        if val == 0:
            return 0
        elif val > 0:
            return 1
        else:
            return 2


    def plot_pareto_landscape(self, resolution, rule_population, plot_rules, color_rules, heros, show=True, save=False, output_path=None):
        # Generate fitness landscape ******************************
        x = np.linspace(0,1.05*self.metric_limits[1],resolution) #coverage
        y = np.linspace(0,1.05,resolution) #accuracy
        Z = [[None for _ in range(resolution)] for _ in range(resolution)]
        for i in range(len(x)):
            for j in range(len(y)):
                Z[j][i] = self.get_pareto_fitness(y[j],x[i],True,heros) #accuracy,coverage  (rows,columns)
        # Prepare to plot rule front *****************************
        metric_1_front_list = [None]*len(self.rule_front_scaled)
        metric_2_front_list = [None]*len(self.rule_front_scaled)
        i = 0
        for rule in self.rule_front_scaled:
            metric_1_front_list[i] = rule[0]
            metric_2_front_list[i] = rule[1]
            i+=1
        # Plot Setup *********************************************
        plt.figure(figsize=(10,6)) #(10, 8))
        plt.imshow(Z, extent=[0, 1.05, 0, 1.05], interpolation='nearest', origin='lower', cmap='magma', aspect='auto') #cmap='viridis' 'magma', alpha=0.6
        # Plot rule front ***************************************
        plt.plot(np.array(metric_2_front_list), np.array(metric_1_front_list), 'o-', ms=10, lw=2, color='black')
        # Plot pareto front boundaries to plot edge [x1,x2], [y1,y2]
        plt.plot([metric_2_front_list[-1],0],[metric_1_front_list[-1],metric_1_front_list[-1]],'--',lw=1, color='black') # Max accuracy line (horizontal)
        plt.plot([metric_2_front_list[0],metric_2_front_list[0]],[metric_1_front_list[0],0],'--',lw=1, color='black') # Max coverage line (vertical)
        # Add colorbar for the gradient
        cbar = plt.colorbar(shrink=0.8)
        cbar.set_label('Fitness Value')
        cbar.set_ticks([0, 0.25, 0.5, 0.75, 1.0])
        cbar.set_ticklabels(['0', '0.25', '0.5', '0.75', '1.0'])
        # Add labels and title
        plt.xlabel('Useful Coverage', fontsize=14)
        plt.ylabel('Useful Accuracy', fontsize=14)
        # Set the axis limits between 0 and 1
        plt.xlim(0, 1.05)
        plt.ylim(0, 1.05)
        def create_x_tick_transform(multiplier):
            def x_tick_transform(x, pos):
                return f"{x * multiplier:.1f}"  # Multiply by value and convert to an integer
            return x_tick_transform
        plt.gca().xaxis.set_major_formatter(FuncFormatter(create_x_tick_transform(self.metric_limits[1])))
        # Prepare to plot rule population ***********************
        if plot_rules:
            if not color_rules:
                master_metric_1_list = []
                master_metric_2_list = []
                for i in range(len(rule_population.pop_set)):
                    rule = rule_population.pop_set[i]
                    master_metric_1_list.append(rule.useful_accuracy)
                    master_metric_2_list.append(rule.useful_coverage/float(self.metric_limits[1]))
                plt.plot(np.array(master_metric_2_list), np.array(master_metric_1_list), 'o', ms=3, lw=1, color='grey')
            else: #plot rules colored by rule specificity.
                color_list = ['yellow','forestgreen','lime','purple','aquamarine','blue','red','blueviolet']
                master_metric_1_list = [[] for _ in range(heros.rsl)]
                master_metric_2_list = [[] for _ in range(heros.rsl)]
                for i in range(len(rule_population.pop_set)):
                    rule = rule_population.pop_set[i]
                    specificity = len(rule.condition_indexes)
                    master_metric_1_list[specificity-1].append(rule.useful_accuracy)
                    master_metric_2_list[specificity-1].append(rule.useful_coverage/float(self.metric_limits[1]))
                for i in range(heros.rsl):
                    try:
                        if i > 8: #indexes of hard coded colors
                            plt.plot(np.array(master_metric_2_list[i]), np.array(master_metric_1_list[i]), 'o', ms=3, lw=1, color='brown', label='Spec: '+str(i+1)) # Accuracy line
                        else:
                            plt.plot(np.array(master_metric_2_list[i]), np.array(master_metric_1_list[i]), 'o', ms=3, lw=1, color=color_list[i], label='Spec: '+str(i+1)) # Accuracy line
                    except:
                        pass
        plt.legend(loc='upper left', bbox_to_anchor=(1.25, 1), fontsize='small')
        plt.subplots_adjust(right=0.75)
        if save:
            plt.savefig(output_path+'/pareto_fitness_landscape_rules.png', bbox_inches="tight")
        if show:
            plt.show()