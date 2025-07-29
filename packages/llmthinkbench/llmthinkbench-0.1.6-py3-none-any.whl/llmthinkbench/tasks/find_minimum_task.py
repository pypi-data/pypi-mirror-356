import random
import logging
from tqdm import tqdm
import os
from ..utils.find_minimum_parsing import parse_find_minimum_answer
from .base_task import BaseTask

class FindMinimumTask(BaseTask):
    """Implementation of the find minimum task"""
    
    @property
    def task_name(self):
        return "find_minimum"
    
    def generate_data(self, list_size, include_negatives=True):
        """Generate random lists of numbers within specified range"""
        
        if self.seed is not None:
            random.seed(self.seed)
            
        data = []
        for _ in range(self.num_samples):
            if include_negatives:
                numbers = random.sample(range(self.min_val, self.max_val + 1), list_size)
            else:
                numbers = random.sample(range(1, self.max_val + 1), list_size)
            data.append(numbers)
        return data
    
    def create_prompt(self, data_point):
        """Create prompt for find minimum task"""
        return (f"Find the minimum number from the given list of numbers. List = {data_point}.\n\n"
                f"Your final answer must be in the format \\boxed{{minimum}} at the end of your response.")
    
    def evaluate_response(self, response, data_point):
        """Evaluate model response for finding minimum task"""
        ground_truth = min(data_point)
        instruction_followed, extracted_answer = parse_find_minimum_answer(response)
        accuracy = 0
        
        try:
            # If parsed answer is correct, set accuracy to 1 regardless of instruction following
            accuracy = 1 if extracted_answer == ground_truth else 0
        except Exception as e:
            logging.debug(f"Comparison error: {e}")
            accuracy = 0
        
        return {
            "input_list": data_point,
            "ground_truth": ground_truth,
            "parsed_min": extracted_answer,
            "accuracy": accuracy,
            "instruction_followed": instruction_followed
        }
    
    def run_evaluation(self, list_sizes, include_negatives=True):
        """Run evaluation for multiple list sizes"""
        all_metrics = []
        
        for list_size in list_sizes:
            logging.info(f"\n{'='*40}\nEvaluating find minimum with list size {list_size} ({'mixed' if include_negatives else 'positive only'} numbers)\n{'='*40}")
            
            # Generate evaluation data
            data = self.generate_data(list_size, include_negatives)
            
            # Run each fold
            for fold in range(1, self.num_folds + 1):
                metrics = self.run_fold(data, list_size, fold)
                metrics['list_size'] = list_size
                metrics['include_negatives'] = include_negatives
                all_metrics.append(metrics)
        
        return all_metrics