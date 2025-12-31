#!/usr/bin/env python

import time
from datetime import datetime
from xml.etree import ElementTree as ET

class TestRunner(object):
    def __init__(self):
        self.results = []

    def run(self, tests):
        print("\nRunning API Tests\n")
        
        for name, func in tests.items():
            start = time.time()
            try:
                func()
                passed = True
                error = None
            except Exception as e:
                passed = False
                error = str(e)
            
            duration = time.time() - start
            self.results.append((name, passed, duration, error))
            
            # Print result
            status = "✓" if passed else "✗"
            color = "\033[32m" if passed else "\033[31m"
            print("{0}{1}\033[0m {2} ({3:.2f}s)".format(color, status, name, duration))
            if error:
                print("\033[31m  {0}\033[0m".format(error))

        # Print summary
        passed = sum(1 for r in self.results if r[1])
        total = len(self.results)
        print("\nTest Results: {0}/{1} passed".format(passed, total))

        # Generate XML report
        suite = ET.Element("testsuite", {
            "name": "API Tests",
            "timestamp": datetime.now().isoformat(),
            "tests": str(total),
            "failures": str(total - passed)
        })
        
        for name, passed, duration, error in self.results:
            case = ET.SubElement(suite, "testcase", {
                "name": name,
                "time": "{0:.3f}".format(duration)
            })
            if not passed:
                failure = ET.SubElement(case, "failure")
                failure.text = error
        
        tree = ET.ElementTree(suite)
        tree.write("report.xml", encoding="utf-8") 