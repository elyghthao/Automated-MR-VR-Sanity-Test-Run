import os
import subprocess
import time
import datetime

import TestrailAPI

# import TestrailAPI


mauiFlash = "maui f -w && adb wait-for-device"
mauiFlashBuild = ""
getFingerprint = "adb shell getprop ro.build.fingerprint"
logcat = "adb logcat --max-count 50"
shellServices = "adb shell service list"
cls = "cls"
rebootToFastboot = "adb reboot bootloader"
rebootToAdbFromFB = "fastboot reboot"
fastbootDevices = "fastboot devices"
adbDevices = "adb devices"
adbReboot = "adb reboot"
waitForAdb = "adb wait-for-device"
bootComplete = "adb shell getprop | grep sys.boot_completed"
adbRoot = "adb root && adb wait-for-device"
unitTest = "adb shell \"syncboss_consumers_ctl stop && syncboss_unit_tests && syncboss_consumers_ctl start && exit\""
updateFirmware = "adb shell \"syncboss_consumers_ctl stop && fw_init --syncboss && syncboss_print_fw_version && syncboss_consumers_ctl start && exit\""
audioCheck = "adb shell audio_tool -m wav_player -s 450 --volume 15"
sensorToolCommand1 = "adb shell sensor_tool -Pdownward-active_slots -PworldTracking-active_slots -Peye-active_slots -Tdownward-codecOnHands-2 -TworldTracking-lowLightHandsDoubleFlood-2 -Teye-utilityNoSequencing-2 -t 10 --exp --gain"
sensorToolCommand2 = "adb shell sensor_tool -Pdownward-active_slots -PworldTracking-active_slots -PworldTracking-hand -Peye-active_slots -Tdownward-codecOnHands-2 -TworldTracking-lowLightHandsFlood-2 -TworldTracking-lowLightHandsDoubleFlood-4 -TworldTracking-lowLightController-6 -Teye-utilityNoSequencing-2 -t 10 --exp --gain"
cameraSetup = "adb root && adb remount && adb shell stop trackingservice mrsystemservice"
slamOnly = "adb shell cameratool -i 0 -i 1 -i 2 -i 3 -t 10"
etOnly = "adb shell cameratool --cascade -t 10"
slamEt = "adb shell cameratool -i 0 -i 1 -i 2 -i 3 -i 6 -i 7 -i 8 -i 9 -t 10"
dtcOnly = "adb shell cameratool -i 4 -i 5 -t 10"
slamDtcEt = "adb shell cameratool -C --cascade -t 10"
vrsRecorder = ""
bluetoothDiscovery = "adb shell am broadcast -a com.oculus.vrbtcontrol.EVENT -n com.oculus.vrbtcontrol/.VrBtControlBroadcastReceiver --es cmd_type ""DISCOVER"""
bluetoothList = "adb logcat -e \"BT discovery: Device: Logi M650 B\" -m 1"
bluetoothGetEvent = "adb shell getevent -c 500"
deviceIdleDisable = "adb shell dumpsys deviceidle disable"
wifiScan = "adb shell cmd wifi status && adb shell cmd wifi set-wifi-enabled enabled && adb shell cmd wifi start-scan && adb shell cmd wifi list-scan-results"
wifiPing = "adb shell \"ping -c 5 -w 10 www.facebook.com\""

curBuild = ""
pathname = ""
resultName = ""
results = ""
runVrsPlayer = ""
planId = ""
testList = {}
useTestrail = True  # change to False when testing -> makes the program not send to testrail api when false
curDevice = ""


def getPlanId():
    return planId



########################################################################
def adbSanityCheck():
    testResult = True

    print("\n\n\n\n\n\n********Verify Device Passes adb/fastboot sanity check********")
    time.sleep(1)
    try:
        subprocess.run(waitForAdb, shell=True)
        print("\n\n\nRunning Logcat")
        logcatOutput = subprocess.getoutput(logcat)
        print(logcatOutput)
        if len(logcatOutput) < 4800:
            testResult = False

        print("\n\n\nRebooting To Fastboot")
        subprocess.run(rebootToFastboot, shell=True)
        time.sleep(10)
        print("\n\n\nListing Fastboot Devices")
        time.sleep(1)
        fastbootOutput = subprocess.getoutput(fastbootDevices)
        print(fastbootOutput)
        if fastbootOutput.lower().count("fastboot") == 0:
            testResult = False

        print("\n\n\nRebooting To ADB")
        subprocess.run(rebootToAdbFromFB, shell=True)
        subprocess.run(waitForAdb, shell=True)
        print("\n\n\nListing ADB Devices")
        time.sleep(5)
        adbDevicesOutput = subprocess.getoutput(adbDevices)
        if adbDevicesOutput.lower().count("device") == 0:  # rewrite this later to include ssn
            testResult = False
    except subprocess.CalledProcessError as e:
        testResult = False

    results.write("\n\nVerify Device Passes adb/fastboot sanity check\n")  ################add test result part
    print("\n\nVerify Device Passes adb/fastboot sanity check")
    if testResult:
        results.write("(Automated)Results-> Passed")
        if useTestrail: TestrailAPI.addTestResult(1, "", "", curBuild,
                                                  testList["Verify device passes adb/fastboot sanity check"], curDevice)
        print("\n(Automated)Results-> Passed")
    else:
        results.write("(Automated)Results-> Failed")
        print("\n(Automated)Results-> Failed")


########################################################################
def bootCom():
    testResult = True
    print("\n\n\n\n\n\n********Verify boot complete returns true********")

    try:
        subprocess.run(waitForAdb, shell=True)
        time.sleep(10)
        bootComOutput = subprocess.getoutput(bootComplete)
        print(bootComOutput)
        if bootComOutput.count("[sys.boot_completed]: [1]") != 1: testResult = False
    except subprocess.CalledProcessError as e:
        testResult = False

    results.write("\n\nVerify boot complete returns true\n")
    print("\n\nVerify boot complete returns true")
    if testResult:
        if useTestrail: TestrailAPI.addTestResult(1, "", "", curBuild, testList["Verify boot complete returns true"], curDevice)
        results.write("(Automated)Results-> Passed")
        print("\n(Automated)Results-> Passed")
    else:
        results.write("(Automated)Results-> Failed")
        print("\n(Automated)Results-> Failed")


########################################################################
def shellServ():
    subprocess.run(waitForAdb, shell=True)
    testResult = True
    print("\n\n\n\n\n\n********Verify Shell services can be listed********")
    time.sleep(2)
    try:
        subprocess.run(shellServices, shell=True)
    except subprocess.CalledProcessError as e:
        testResult = False

    time.sleep(1)
    results.write("\n\nVerify shell services can be listed\n")
    print("\n\nVerify shell services can be listed")
    if testResult:
        if useTestrail: TestrailAPI.addTestResult(1, "", "", curBuild, testList["Verify shell services can be listed"], curDevice)
        results.write("(Automated)Results-> Passed")
        print("\n(Automated)Results-> Passed")
    else:
        results.write("(Automated)Results-> Failed")
        print("\n(Automated)Results-> Failed")


########################################################################
def updateFirm():
    subprocess.run(waitForAdb, shell=True)
    testResult = True
    print("\n\n\n\n\n\n********Verify user can update firmware********")
    time.sleep(1)
    try:
        subprocess.run(adbRoot, shell=True)
        firmwareOutput = subprocess.getoutput(updateFirmware)
        print(firmwareOutput)
        print(firmwareOutput.count("100.0%"))
        if firmwareOutput.count("100.0%") == 0: testResult = False
    except subprocess.CalledProcessError as e:
        testResult = False

    print("\n\nVerify user can update firmware")
    results.write("\n\nVerify user can update firmware\n")
    if testResult:
        if useTestrail: TestrailAPI.addTestResult(1, "", "", curBuild, testList["Verify user can update firmware"], curDevice)
        results.write("(Automated)Results-> Passed")
        print("\n(Automated)Results-> Passed")
    else:
        results.write("(Automated)Results-> Failed")
        print("\n(Automated)Results-> Failed")


########################################################################
def syncBossUnit():
    subprocess.run(waitForAdb, shell=True)
    testResult = True
    print("\n\n\n\n\n\n********Verify device passes syncboss unit tests********")

    try:
        subprocess.run(adbRoot)
        unitTestOutput = subprocess.getoutput(unitTest)
        if unitTestOutput.count("[  PASSED  ] 7 tests.") == 0: testResult = False
        print(unitTestOutput)
    except subprocess.CalledProcessError as e:
        testResult = False

    print("\n\nVerify device passes syncboss unit tests")
    results.write("\n\nVerify device passes syncboss unit tests\n")
    if testResult:
        if useTestrail: TestrailAPI.addTestResult(1, "", "", curBuild,
                                                  testList["Verify device passes syncboss unit tests"], curDevice)
        results.write("(Automated)Results-> Passed")
        print("\n(Automated)Results-> Passed")
    else:
        results.write("(Automated)Results-> Failed")
        print("\n(Automated)Results-> Failed")


#############################################################################
def wifiSanity():
    subprocess.run(waitForAdb, shell=True)
    testResult = True
    print("\n\n\n\n\n\n********Verify device passes wifi sanity check********")

    try:
        print("\nRestarting...")
        subprocess.run(adbReboot, shell=True)
        subprocess.run(waitForAdb, shell=True)
        subprocess.run(adbRoot)
        subprocess.run("adb shell \"rm -rf /data/misc/wifi\"")
        print("Waiting for wifi service...")
        time.sleep(10)
        subprocess.run(deviceIdleDisable, shell=True)
        print("\nStarting Scan...")
        subprocess.run(wifiScan, shell=True)
        time.sleep(2)
        # ssid = input("\n\nEnter wifi ssid (network name)-> ")
        ssid = "metaguest"
        # password = input("\n\nEnter password-> ")
        password = "effici3ncy"
        # wifiConnect = "adb shell cmd wifi connect-network " + ssid + " wpa2 " + password + " && ping www.facebook.com"
        wifiConnect = "adb shell cmd wifi connect-network " + ssid + " wpa2 " + password
        print("Connecting to metaguest")
        subprocess.run(wifiConnect, shell=True)
        print("Pinging 'www.facebook.com'...")
        time.sleep(5)
        pingOutput = subprocess.getoutput(wifiPing)
        print(pingOutput)
        # print(pingOutput.count("5 packets transmitted, 5 received, 0% packet loss"))

        if pingOutput.count("facebook.com") != 7: testResult = False
    except subprocess.CalledProcessError as e:
        testResult = False

    print("\n\nVerify device passes wifi sanity check")
    results.write("\n\nVerify device passes wifi sanity check\n")
    if testResult:
        if useTestrail: TestrailAPI.addTestResult(1, "", "", curBuild,
                                                  testList["Verify device passes wifi sanity check"], curDevice)
        results.write("(Automated)Results-> Passed")
        print("\n(Automated)Results-> Passed")
    else:
        results.write("(Automated)Results-> Failed")
        print("\n(Automated)Results-> Failed")


#############################################################################
def bluetoothSanity():
    subprocess.run(waitForAdb, shell=True)
    testResult = True
    print("\n\n\n\n\n\n********Verify device passes Bluetooth Sanity Check********")
    time.sleep(1)
    print("Restarting...")
    subprocess.run(adbReboot, shell=True) #uncomment this later
    subprocess.run(waitForAdb,shell=True)
    subprocess.run(adbRoot, shell=True)
    print("\n\n-Put Bluetooth device into pairing mode")
    time.sleep(2)
    input("\nPress enter when ready")
    subprocess.run(bluetoothDiscovery, shell=True)
    time.sleep(2)
    bluetoothListOutput = subprocess.getoutput(bluetoothList)
    print("bluetooth output: " + bluetoothListOutput)

    btAddrLine = bluetoothListOutput.find("btAddr") # get line with logi mouse
    bluetoothCode = bluetoothListOutput[btAddrLine + 8:btAddrLine + 25] #acquire associated bt address
    print("bluetooth Code: " + bluetoothCode)

    bluetoothPair = "adb shell am broadcast -a com.oculus.vrbtcontrol.EVENT -n com.oculus.vrbtcontrol/.VrBtControlBroadcastReceiver --es cmd_type ""PAIR"" --es bd_addr \"\" " + bluetoothCode + "\"\""
    bluetoothUnpair = "adb shell am broadcast -a com.oculus.vrbtcontrol.EVENT -n com.oculus.vrbtcontrol/.VrBtControlBroadcastReceiver --es cmd_type ""UNPAIR"" --es bd_addr \"\"" + bluetoothCode + "\"\""
    time.sleep(5)
    subprocess.run(bluetoothPair, shell=True)
    time.sleep(2)
    subprocess.run(bluetoothPair, shell=True)
    print("Verify Bluetooth device input by moving device")
    subprocess.run(bluetoothGetEvent,shell=True)
    print("\nUnpairing bluetooth device...")
    time.sleep(2)
    subprocess.run(bluetoothUnpair, shell=True)






    print("\n\nVerify device passes Bluetooth sanity check")
    results.write("\n\nVerify device passes Bluetooth sanity check\n")
    testResultOutput = input("Test Result ->")
    if testResultOutput.lower().count("pass") == 0: testResult = False

    if testResult:
        if useTestrail: TestrailAPI.addTestResult(1, "", "", curBuild, testList[
            "Verify device passes Bluetooth sanity check"], curDevice)
        results.write("(Automated)Results-> Passed")
        print("\n(Automated)Results-> Passed")
    else:
        results.write("(Automated)Results-> Failed")
        print("\n(Automated)Results-> Failed")


########################################################################
def sensorTool():
    subprocess.run(waitForAdb, shell=True)
    testResult = True
    print("\n\n\n\n\n\n********Sensor Tool Validation********")
    try:
        print("Quickly restarting...")
        subprocess.run(adbReboot, shell=True)
        subprocess.run(waitForAdb, shell=True)
        subprocess.run(cameraSetup, shell=True)
        print(
            "\n\nSensor Tool Validation: Command 1----------------------------------------------------------------------------")
        command1Output = subprocess.getoutput(sensorToolCommand1)
        print(command1Output.count("frames dropped: 0"))
        if command1Output.count("frames dropped: 0") != 3: testResult = False
        print(command1Output)

        print(
            "\n\nSensor Tool Validation: Command 2----------------------------------------------------------------------------")
        command2Output = subprocess.getoutput(sensorToolCommand2)
        if command2Output.count("frames dropped: 0") != 3: testResult = False
        print(command2Output)

    except subprocess.CalledProcessError as e:
        testResult = False

    print("\n\nSensor Tool Validation")
    results.write("\n\nSensor Tool Validation\n")
    if testResult:
        if useTestrail: TestrailAPI.addTestResult(1, "", "", curBuild, testList["Sensor Tool Validation"], curDevice)
        results.write("(Automated)Results-> Passed")
        print("\n(Automated)Results-> Passed")
    else:
        results.write("(Automated)Results-> Failed")
        print("\n(Automated)Results-> Failed")


########################################################################
def camTool():
    testResult = True
    subprocess.run(waitForAdb, shell=True)

    try:
        print("\n\n\n\n\n\n********Camera Tool Validation********")
        subprocess.run(cameraSetup, shell=True)
        print(
            "\n\nCamera Tool Validation: SLAM Only----------------------------------------------------------------------------")
        slamOutput = subprocess.getoutput(slamOnly)
        print(slamOutput)
        if slamOutput.count("frames dropped: 0") != 4: testResult = False

        print(
            "\n\nCamera Tool Validation: ET Only----------------------------------------------------------------------------")
        etOutput = subprocess.getoutput(etOnly)
        print(etOutput)
        if etOutput.count("frames dropped: 0") != 4: testResult = False

        print(
            "\n\nCamera Tool Validation: SLAM + ET Only----------------------------------------------------------------------------")
        time.sleep(1)
        slamEtOutput = subprocess.getoutput(slamEt)
        print(slamEtOutput)
        if slamEtOutput.count("frames dropped: 0") != 8: testResult = False

        print(
            "\n\nCamera Tool Validation: DTC Only----------------------------------------------------------------------------")
        time.sleep(1)
        dtcOutput = subprocess.getoutput(dtcOnly)
        print(dtcOutput)
        if dtcOutput.count("frames dropped: 0") != 2: testResult = False

        print(
            "\n\nCamera Tool Validation: SLAM + DTC + ET Only----------------------------------------------------------------------------")
        time.sleep(1)
        slamDtcEtOutput = subprocess.getoutput(slamDtcEt)
        print(slamDtcEtOutput)
        if slamDtcEtOutput.count("frames dropped: 0") != 10: testResult = False

    except subprocess.CalledProcessError as e:
        testResult = False

    print("\n\nCamera Tool Validation")
    results.write("\n\nCamera Tool Validation\n")
    if testResult:
        if useTestrail: TestrailAPI.addTestResult(1, "", "", curBuild, testList["Camera Tool Validation"], curDevice)
        results.write("(Automated)Results-> Passed")
        print("\n(Automated)Results-> Passed")
    else:
        results.write("(Automated)Results-> Failed")
        print("\n(Automated)Results-> Failed")


#######################################################################
def vrsRec():
    if os.path.exists(pathname + "\\default.vrs "):
        subprocess.run(runVrsPlayer, shell=True)
        os.remove(pathname + "\\default.vrs ")

    testResult = True
    subprocess.run(waitForAdb, shell=True)

    try:

        vrsRecorder = " adb shell vrs-recorder --sensoraccess_purposes=downward/active_slots,worldTracking/active_slots  --cmm_allowed_mux_modes=downward/codecOnHands,worldTracking/lowLightHands --duration=2 --headset_magnetometer=false --slam_magnetometer=false --slam_static_exposure_ms=1 --slam_static_gain=4 --downward_static_exposure_ms=1 --downward_static_gain=4 && adb pull /data/misc/default.vrs " + pathname
        print("\n\n\n\n\n\n********Verify VRS Recorder - Worldtracking + downward + imu + static exposure/gain********")
        print("Quickly restarting...")
        subprocess.run(adbReboot, shell=True)
        subprocess.run(waitForAdb, shell=True)
        subprocess.run(cameraSetup, shell=True)
        print("\n\nRunning VRS Recorder command...")
        time.sleep(2)
        subprocess.run(vrsRecorder, shell=True)
        if os.path.exists(pathname + "\\default.vrs "):
            # subprocess.run(runVrsPlayer, shell=True)
            os.remove(pathname + "\\default.vrs ")
        else:
            testResult = False

    except subprocess.CalledProcessError as e:
        testResult = False

    print("\n\nVerify VRS Recorder - Worldtracking + downward + imu + static exposure/gain")
    results.write("\n\nVerify VRS Recorder - Worldtracking + downward + imu + static exposure/gain\n")
    if testResult:
        if useTestrail: TestrailAPI.addTestResult(1, "", "", curBuild, testList[
            "Verify VRS Recorder - Worldtracking + downward + imu + static exposure/gain"], curDevice)
        results.write("(Automated)Results-> Passed")
        print("\n(Automated)Results-> Passed")
    else:
        results.write("(Automated)Results-> Failed")
        print("\n(Automated)Results-> Failed")


########################################################################
def audioSanity():
    testResult = True
    subprocess.run(waitForAdb, shell=True)
    print("\n\n\n\n\n\n********Verify device passes audio sanity check********")
    print("\nThis test case will not end on its own, be sure to end it manually")
    time.sleep(3)
    subprocess.run(audioCheck, shell=True)




    print("\n\nVerify device passes audio sanity check")
    results.write("\n\nVerify device passes audio sanity check\n")
    testResultOutput = input("Test Result ->")
    if testResultOutput.lower().count("pass") == 0: testResult = False

    if testResult:
        if useTestrail: TestrailAPI.addTestResult(1, "", "", curBuild, testList[
            "Verify device passes audio sanity check"], curDevice)
        results.write("(Automated)Results-> Passed")
        print("\n(Automated)Results-> Passed")
    else:
        results.write("(Automated)Results-> Failed")
        print("\n(Automated)Results-> Failed")


def rubyController():
    testResult = True

    ctlStop = "adb shell syncboss_consumers_ctl stop"
    unpairAllControllers = "adb shell syncboss_input_tool --unpair-all"
    pairControllers = "adb shell syncboss_input_tool --pair"
    listPairedControllers = "adb shell syncboss_input_tool --list"

    print("\n\n********Verify device can pair with Crystal(Ruby) controllers********")
    results.write("\n\nVerify device can pair with Crystal(Ruby) controllers\n")
    time.sleep(2)

    try:
        subprocess.run(adbRoot, shell=True)
        subprocess.run(ctlStop,shell=True)
        print("Unpairing current controllers")
        print("Press Enter")
        subprocess.run(unpairAllControllers,shell=True)
        print("\n\n\nPut the Crystal controllers in pairing mode  (“Menu” button + “Y” for left, and “Meta” button + “B” for right)")
        time.sleep(1)
        input("Press enter when ready")


        subprocess.run(pairControllers,shell=True)
        print("\nNow pair the other controller")
        subprocess.run(pairControllers, shell=True)

        print("Listing Paired Controllers")
        subprocess.run(listPairedControllers,shell=True)


    except subprocess.CalledProcessError as e:
        testResult = False

    print("\n\nVerify device can pair with Crystal(Ruby) controllers")
    results.write("\n\nVerify device can pair with Crystal(Ruby) controllers\n")
    testResultOutput = input("Test Result ->")
    if testResultOutput.lower().count("pass") == 0: testResult = False

    if testResult:
        if useTestrail: TestrailAPI.addTestResult(1, "", "", curBuild, testList[
            "Verify device can pair with Crystal(Ruby) controllers"], curDevice)
        results.write("(Automated)Results-> Passed")
        print("\n(Automated)Results-> Passed")
    else:
        results.write("(Automated)Results-> Failed")
        print("\n(Automated)Results-> Failed")

def adbInstallPlay():
    testResult = True
    print("\n\n********Verify apps are able to be installed/launched in shell via adb commands********")
    results.write("\n\nVerify apps are able to be installed/launched in shell via adb commands\n")
    time.sleep(2)


    try:
        print()
        input("Be in VR Home. Press enter when ready.")
        print("\nInstalling Laser Sword")
        subprocess.run("adb install C:\\Users\\thaoelygh\\Desktop\\laser-sword.apk", shell=True)
        time.sleep(1)
        packagesOutput = subprocess.getoutput("adb shell pm list packages")
        print(packagesOutput)
        if packagesOutput.count("com.XRVerification.LaserSword") < 1:
            testResult = False
        else:
            print("\nStarting Shell")
            subprocess.run(adbRoot)
            subprocess.run("adb shell am broadcast -a com.oculus.vrpowermanager.prox_close")
            time.sleep(5)
            subprocess.run("adb shell am startservice -a nux.ota.SKIP_NUX -n com.oculus.nux.ota/.NuxOtaIntentService")
            time.sleep(12)
            subprocess.run(waitForAdb)
            subprocess.run("adb shell am broadcast -a com.oculus.vrpowermanager.prox_close")
            time.sleep(5)
            print("\nStarting App")
            subprocess.run("adb shell monkey -p com.XRVerification.LaserSword 1",shell=True)

    except subprocess.CalledProcessError as e:
        testResult = False

    print("\n\nVerify apps are able to be installed/launched in shell via adb commands")
    results.write("\n\nVerify apps are able to be installed/launched in shell via adb commands\n")


    if testResult:
        if useTestrail: TestrailAPI.addTestResult(1, "", "", curBuild, testList[
            "Verify apps are able to be installed/launched in shell via adb commands"], curDevice)
        results.write("(Automated)Results-> Passed")
        print("\n(Automated)Results-> Passed")
    else:
        results.write("(Automated)Results-> Failed")
        print("\n(Automated)Results-> Failed")




def wifiCast():
    testResult = True

    print("\n\n********Verify Wifi casting passes********")
    results.write("\n\nVerify Wifi casting passes\n")
    time.sleep(2)

    try:
        print("Restarting...")
        subprocess.run(adbReboot,shell=True)
        subprocess.run(waitForAdb,shell=True)
        subprocess.run(adbRoot,shell=True)
        subprocess.run("adb shell \"rm -rf /data/misc/wifi\"")
        print("Waiting for wifi service...")
        time.sleep(10)
        subprocess.run(deviceIdleDisable, shell=True)
        print("\n\nMake sure iPhone hotspot is setup")
        input("Press when Ready")
        print("\nStarting Scan...")
        time.sleep(1)
        subprocess.run(wifiScan, shell=True)
        time.sleep(5)
        ssid = "iPhone"
        password = "elyghthao"
        wifiConnect = "adb shell cmd wifi connect-network " + ssid + " wpa2 " + password
        # subprocess.run("ipconfig")
        print("Connecting to iPhone")
        subprocess.run(wifiConnect, shell=True)

        verify = True
        while verify:
            print("\n\n\n\n\nVerify Connection: ")
            subprocess.run("adb shell cmd wifi status", shell=True)
            if len(input("\n\nIf correct -> enter any text, then press enter. To try again -> press enter\n")) == 0:
                print("\nStarting Scan...")
                time.sleep(1)
                subprocess.run(wifiScan, shell=True)
                time.sleep(5)
                subprocess.run(wifiConnect, shell=True)
                continue
            verify = False


        ip = "172.20.10.1"
        time.sleep(2)
        print("Pinging Router")
        time.sleep(3)
        subprocess.run("adb shell ping -s 2000 -c 300 -i 0.001 " + ip,shell = True)


    except subprocess.CalledProcessError as e:
        testResult = False

    print("\n\nVerify Wifi casting passes")
    results.write("\n\nVerify Wifi casting passes\n")
    testResultOutput = input("Test Result ->")
    if testResultOutput.lower().count("pass") == 0: testResult = False

    if testResult:
        if useTestrail: TestrailAPI.addTestResult(1, "", "", curBuild, testList[
            "Verify Wifi casting passes"], curDevice)
        results.write("(Automated)Results-> Passed")
        print("\n(Automated)Results-> Passed")
    else:
        results.write("(Automated)Results-> Failed")
        print("\n(Automated)Results-> Failed")

if __name__ == '__main__':
    import sys



    curBuild = input("Enter Build (Please enter the longer version please) ->")
    planId = input("Enter Plan ID ->")
    curDevice = input("Enter Device ->")
    useTestrail = False #######################################################################

    if useTestrail: testList = TestrailAPI.getTests(planId)
    now = datetime.datetime.now()
    formatted_date = now.strftime("%m-%d-%y")
    formatted_time = now.strftime("%Hh%Mm%Ss")
    curTime = formatted_date + "   "
    file = sys.argv[0]
    pathname = os.path.dirname(file)
    resultName = "" + pathname + "\\" + curDevice + " " + curBuild + "  " + curTime + ".txt"
    results = open(resultName, 'w')
    results.write("" + curDevice)
    results.write("\nTEST RESULTS for " + curBuild + ": " + curTime + "\n\n\n")
    runVrsPlayer = "" + pathname + "\\vrsplayer.exe " + pathname + "\\default.vrs"
    time.sleep(1)
    print("Enter ONLY RESULT after each test case -->Pass/Fail")
    time.sleep(1)
    print("Using Testrail API: " + str(useTestrail) )
    time.sleep(1)
    print("\nStarting Test Run...")
    subprocess.run(waitForAdb,shell=True)
    time.sleep(1)

    # flashingMaui()  # fully automated
    adbSanityCheck()  # fully automated
    bootCom()  # fully automated
    shellServ()  # fully automated
    updateFirm()  # fully automated
    syncBossUnit()  # fully automated
    wifiSanity()  # fully automated
    sensorTool()  # fully automated
    camTool()  # fully automated
    vrsRec()  # fully automated

    rubyController()
    wifiCast()
    audioSanity()
    bluetoothSanity() #semi automated, will be ran at the very end

    # adbInstallPlay() #start VR Shell test cases

    #add manual Tests here too