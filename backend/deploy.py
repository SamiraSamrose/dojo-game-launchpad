# backend/deploy.py
# Deployment and testing scripts

import os
import sys
import logging
from sqlalchemy import create_engine
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def init_database():
    """Initialize database with tables and seed data"""
    print("🔧 Initializing Database...")
    
    from backend.models import Base, User
    
    DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://dojo_user:dojo_pass@localhost:5432/dojo_launchpad")
    engine = create_engine(DATABASE_URL)
    
    # Create all tables
    Base.metadata.create_all(bind=engine)
    print("✅ Database tables created")
    
    # Seed initial data
    from sqlalchemy.orm import sessionmaker
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()
    
    try:
        # Create admin user
        admin = User(
            username="admin",
            email="admin@dojogames.io",
            wallet_address="0x0000000000000000000000000000000000000000"
        )
        db.add(admin)
        db.commit()
        print("✅ Admin user created")
        
    except Exception as e:
        print(f"❌ Error seeding data: {e}")
        db.rollback()
    finally:
        db.close()
    
    print("🎉 Database initialization complete!")


def run_tests():
    """Run all tests"""
    import subprocess
    print("🧪 Running tests...")
    result = subprocess.run(["pytest", "-v", "backend/tests/"], capture_output=True, text=True)
    print(result.stdout)
    if result.returncode != 0:
        print("❌ Tests failed")
        sys.exit(1)
    print("✅ All tests passed")


def load_test(endpoint="/", num_requests=100):
    """Load test an endpoint"""
    import requests
    import time
    from concurrent.futures import ThreadPoolExecutor
    
    print(f"\n🔥 Load Testing: {endpoint}")
    print(f"Requests: {num_requests}")
    
    base_url = "http://localhost:8000"
    
    def make_request():
        try:
            start = time.time()
            response = requests.get(f"{base_url}{endpoint}")
            duration = time.time() - start
            return duration, response.status_code
        except Exception as e:
            return None, str(e)
    
    start_time = time.time()
    
    with ThreadPoolExecutor(max_workers=10) as executor:
        results = list(executor.map(lambda _: make_request(), range(num_requests)))
    
    total_time = time.time() - start_time
    
    # Calculate statistics
    successful = [r for r in results if r[1] == 200]
    durations = [r[0] for r in successful if r[0] is not None]
    
    print(f"\n📊 Results:")
    print(f"  Total time: {total_time:.2f}s")
    print(f"  Successful: {len(successful)}/{num_requests}")
    print(f"  Avg response time: {sum(durations)/len(durations)*1000:.2f}ms")
    print(f"  Min response time: {min(durations)*1000:.2f}ms")
    print(f"  Max response time: {max(durations)*1000:.2f}ms")
    print(f"  Requests/sec: {num_requests/total_time:.2f}")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        if command == "init":
            init_database()
        elif command == "test":
            run_tests()
        elif command == "load-test":
            endpoint = sys.argv[2] if len(sys.argv) > 2 else "/"
            num_requests = int(sys.argv[3]) if len(sys.argv) > 3 else 100
            load_test(endpoint, num_requests)
        else:
            print(f"Unknown command: {command}")
    else:
        print("""
╔══════════════════════════════════════════════════════════════╗
║         DOJO LAUNCHPAD - DEPLOYMENT TOOLS                    ║
║                                                              ║
║  Commands:                                                   ║
║    python backend/deploy.py init         - Initialize DB    ║
║    python backend/deploy.py test         - Run tests        ║
║    python backend/deploy.py load-test    - Load test API    ║
╚══════════════════════════════════════════════════════════════╝
        """)
