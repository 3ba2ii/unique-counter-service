import concurrent.futures
import time
from typing import Set, Dict, Any
from url_generator import ShortCodeGenerator

class ConcurrentTester:
    def __init__(self, num_users: int, max_retries: int = 3):
        self.num_users = num_users
        self.max_retries = max_retries
        self.generator = ShortCodeGenerator()
        self.generated_codes: Set[str] = set()
        
    def generate_code_with_retry(self) -> str:
        for attempt in range(self.max_retries):
            try:
                return self.generator.generate_code()
            except Exception as e:
                if attempt == self.max_retries - 1:
                    raise e
                time.sleep(0.1)
    
    def run_test(self) -> Dict[str, Any]:
        start_time = time.time()
        success_count = 0
        failure_count = 0
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=self.num_users) as executor:
            future_to_user = {
                executor.submit(self.generate_code_with_retry): i 
                for i in range(self.num_users)
            }
            
            for future in concurrent.futures.as_completed(future_to_user):
                user_id = future_to_user[future]
                try:
                    code = future.result()
                    if code in self.generated_codes:
                        print(f"❌ Duplicate code detected: {code}")
                        failure_count += 1
                    else:
                        self.generated_codes.add(code)
                        print(f"✅ User {user_id} generated code: {code}")
                        success_count += 1
                except Exception as e:
                    print(f"❌ User {user_id} failed: {str(e)}")
                    failure_count += 1

        end_time = time.time()
        total_time = end_time - start_time
        
        return {
            "total_time": total_time,
            "unique_codes": len(self.generated_codes),
            "expected_codes": self.num_users,
            "success_rate": (success_count / self.num_users) * 100,
            "success_count": success_count,
            "failure_count": failure_count
        }

def main():
    NUM_USERS = 1000
    tester = ConcurrentTester(NUM_USERS)
    results = tester.run_test()
    
    print(f"\nTest Summary:")
    print(f"Total time: {results['total_time']:.2f} seconds")
    print(f"Total unique codes generated: {results['unique_codes']}")
    print(f"Expected codes: {results['expected_codes']}")
    print(f"Success rate: {results['success_rate']:.2f}%")
    print(f"Successful generations: {results['success_count']}")
    print(f"Failed generations: {results['failure_count']}")

if __name__ == "__main__":
    main() 