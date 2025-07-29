import random
import logging
from .base_task import BaseTask
from ..utils.absolute_difference_parsing import parse_absolute_difference_answer

class AbsoluteDifferenceTask(BaseTask):
    """Implementation of the absolute difference task"""
    
    @property
    def task_name(self):
        return "absolute_difference"
    
    def generate_data(self, list_size=2):
        """Generate random pairs of numbers for calculating absolute difference"""

        if self.seed is not None:
            random.seed(self.seed)
            
        if list_size != 2:
            raise ValueError("Absolute difference task requires exactly 2 numbers.")
            
        data = []
        include_negatives = True  # Based on your original code
        
        for _ in range(self.num_samples):
            if include_negatives:
                numbers = random.sample(range(self.min_val, self.max_val + 1), list_size)
            else:
                numbers = random.sample(range(1, 101), list_size)
            data.append(numbers)
        
        return data
    
    def create_prompt(self, data_point):
        """Create prompt for absolute difference task"""
        return (f"Find the absolute difference between the following list of numbers: \n{data_point}\n\n"
                f"Provide the result. Your final answer must be in the format \\boxed{{answer}} at the end.")
    
    def evaluate_response(self, response, data_point):
        """Evaluate model response for absolute difference task"""
        ground_truth = abs(data_point[1] - data_point[0])
        instruction_followed, answer = parse_absolute_difference_answer(response)
        accuracy = 0
        
        if (ground_truth == answer):
            accuracy = 1
        
        return {
            "input_numbers": data_point,
            "ground_truth": ground_truth,
            "parsed_answer": answer,
            "accuracy": accuracy,
            "instruction_followed": instruction_followed
        }
    
    def run_evaluation(self, list_sizes=None):
        """Run evaluation for absolute difference task"""
        all_metrics = []
        list_size = 2  # Absolute difference always uses 2 numbers
        
        logging.info(f"\n{'='*40}\nEvaluating absolute difference task\n{'='*40}")
        
        # Generate evaluation data
        data = self.generate_data(list_size)
        
        # Run each fold
        for fold in range(1, self.num_folds + 1):
            metrics = self.run_fold(data, "absolute_difference", fold)
            metrics['list_size'] = list_size
            all_metrics.append(metrics)
        
        return all_metrics