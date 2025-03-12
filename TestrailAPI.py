import subprocess

import testrail

# Create a TestRail API client instance
client = testrail.APIClient("https://rl-test.com/")
client.user = "thaoelygh@meta.com"
client.password = "23zQ/Wy8ZSpM9zg2uUXx-dsRTAL3lrl.ufe2LpCGf"



def getTestResults(test_id): #'status_id': 1-Passed, 2-Blocked, 4-Retest, 5-Failed, 6-NotApplicable, 7-NotYetImplemented, 8-Warned, 9-Assigned
    testResult = client.send_get("get_results/" + str(test_id))
    # print(testResult)
    return testResult


# #get test
# test = client.send_get("get_test/" + "4586233693")
# print(test)


def addTestResult (status_id,comment,defects,version,test_id,custom_device):#'status_id': 1-Passed, 2-Blocked, 4-Retest, 5-Failed, 6-NotApplicable, 7-NotYetImplemented, 8-Warned, 9-Assigned
    request_body = {
        "status_id": status_id,
        "comment": str(comment),
        "elapsed": "",
        "defects": str(defects),
        "version": str(version),
        "custom_device":custom_device,
    }
    addTest = client.send_post("add_result/"+str(test_id), request_body)


# # #get all test from test run (requires test run id) (not test plan)
# getRun = client.send_get("get_tests/" + "997027")
# # print(getRun)
# for a in getRun.get('tests'):
#     print(a.get('id') , " " + a.get('title'))


#get test suite runs from test plan (requires test plan id)
# getPlan = client.send_get("get_plan/" + "997026")
# print(getPlan)
# for a in getPlan.get('entries'):
#     print(a.get('runs')[0].get('id') , " " + a.get('runs')[0].get('name'))



def getTests(planId): ##takes in id of test plan, returns all tests and their test id -> key=name, value=test_id
    plan = client.send_get("get_plan/" + str(planId))
    testSuiteRuns = []
    tests = {}
    #get all test runs/suites
    for a in plan.get('entries'):
        testSuiteRuns.append(a.get('runs')[0].get('id'))
    #get all tests from test runs/suites
    # print(testSuiteRuns)
    for a in testSuiteRuns:
        # print(client.send_get("get_tests/" + str(a)))
        run = client.send_get("get_tests/" + str(a))
        # print(run)
        for b in run.get('tests'):
            tests[b.get('title')] = b.get('id')
    # print(tests)
    return tests #returns a dict


def CTP(plan_1_id,plan_2_id,newVersion, device): #not working/ from plan1 to plan 2
    plan1 = getTests(plan_1_id)
    plan2 = getTests(plan_2_id)
    for key,value in plan1.items():
        result = client.send_get("get_results/" + str(value))['results'][0]
        # result = getTestResults(value)['results'][0]
        addTestResult(result['status_id'], result['comment'], result['defects'], newVersion, plan2[key], device)
        print(key)





if __name__ == '__main__':
    print("elygh")
    # print(getTests("997026"))
    # CTP("1016395", "1018874", "3778.3490.1301", "Pismo P1 HMD")

    # print(getTestResults(4593153798))
    # print(addTestResult(1,"","",1234,4591751987,"Pismo P1"))

    # ipconfigOutput = subprocess.getoutput("ipconfig")
    # print(ipconfigOutput)







