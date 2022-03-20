using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using DG.Tweening;
using UnityEngine.UI;

//using LockingPolicy = Thalmic.Myo.LockingPolicy;
//using Pose = Thalmic.Myo.Pose;
//using UnlockType = Thalmic.Myo.UnlockType;
//using VibrationType = Thalmic.Myo.VibrationType;

public class CanvasController : MonoBehaviour
{
    public GameObject Canvas;
    private Image background;
    //private Slider leftslider;
    //private Slider rightslider;
    private SceneManager scene;

    public Man rightman;
    public Man leftman;

    // Myo game object to connect with.
    // This object must have a ThalmicMyo script attached.
    //public GameObject myo = null;
    //private Pose _lastPose = Pose.Unknown;


    // Start is called before the first frame update
    void Start()
    {
        Canvas = GameObject.Find("Canvas");
        //background = Canvas.transform.Find("background").GetComponent<Image>();
        //leftslider= Canvas.transform.Find("leftlegChange").GetComponent<Slider>();
        //rightslider = Canvas.transform.Find("rightlegChange").GetComponent<Slider>();
        scene = GetComponent<SceneManager>();
        //ReInit();
    }

    // Update is called once per frame
    void Update()
    {
        // Access the ThalmicMyo component attached to the Myo game object.
        //ThalmicMyo thalmicMyo = myo.GetComponent<ThalmicMyo>();

        //// Check if the pose has changed since last update.
        //// The ThalmicMyo component of a Myo game object has a pose property that is set to the
        //// currently detected pose (e.g. Pose.Fist for the user making a fist). If no pose is currently
        //// detected, pose will be set to Pose.Rest. If pose detection is unavailable, e.g. because Myo
        //// is not on a user's arm, pose will be set to Pose.Unknown.
        //if (thalmicMyo.pose != _lastPose)
        //{
        //    _lastPose = thalmicMyo.pose;

        //    // Vibrate the Myo armband when a fist is made.
        //    if (thalmicMyo.pose == Pose.Fist)
        //    {
        //        //thalmicMyo.Vibrate(VibrationType.Medium);
        //        //print("F");

        //        //if (leftman.isLegOn)
        //        //{
        //        //    leftman.UpLeg();
        //        //    rightman.UpLeg();
        //        //}
        //        //else
        //        //{
        //        //    leftman.DownLeg();
        //        //    rightman.DownLeg();
        //        //}
        //        print("Down");
        //        //rightman.DownLeg();
        //        //leftman.DownLeg();

        //        //if (rightman.isLegOn)
        //        //{
        //        //    rightman.UpLeg();
        //        //}
        //        //else
        //        //{
        //        //    rightman.DownLeg();
        //        //}

        //        ExtendUnlockAndNotifyUserAction(thalmicMyo);

        //        // Change material when wave in, wave out or double tap poses are made.
        //    }
        //    else if (thalmicMyo.pose == Pose.FingersSpread)
        //    {
        //        //GetComponent<Renderer>().material = waveInMaterial;
        //        //print("hi");

        //        //print("Up");
        //        //if (leftman.isLegOn)
        //        //{
        //        //    leftman.UpLeg();
        //        //}
        //        //else
        //        //{
        //        //    leftman.DownLeg();
        //        //}
        //        //rightman.UpLeg();
        //        //leftman.UpLeg();

        //        ExtendUnlockAndNotifyUserAction(thalmicMyo);
        //    }
        //    else if (thalmicMyo.pose == Pose.WaveIn)
        //    {
        //        //print("L");
        //        //if (leftman.isLegOn)
        //        //{
        //        //    leftman.UpLeg();
        //        //}
        //        //else
        //        //{
        //        //    leftman.DownLeg();
        //        //}
        //        //GetComponent<Renderer>().material = waveInMaterial;

        //        ExtendUnlockAndNotifyUserAction(thalmicMyo);
        //    }
        //    else if (thalmicMyo.pose == Pose.WaveOut)
        //    {
               

        //        //GetComponent<Renderer>().material = waveOutMaterial;

        //        ExtendUnlockAndNotifyUserAction(thalmicMyo);
        //    }
        //    else if (thalmicMyo.pose == Pose.DoubleTap)
        //    {
        //        //GetComponent<Renderer>().material = doubleTapMaterial;
               

        //        ExtendUnlockAndNotifyUserAction(thalmicMyo);
        //    }
        //}
    }

    public void FadeBackGround(GameObject fademan, GameObject showman)
    {        
        StartCoroutine(startfade(0.5f, fademan, showman));
    }

    IEnumerator startfade(float fadetime,GameObject fademan,GameObject showman)
    {
        scene.canoperate = false;
        background.DOFade(1, fadetime);
        yield return new WaitForSeconds(fadetime);
        fademan.SetActive(false);
        showman.SetActive(true);
        background.DOFade(0, fadetime);
        //ReInit();
        yield return new WaitForSeconds(fadetime);       
        scene.canoperate = true;
    }

    //public void ReInit()
    //{
    //    leftslider.value = scene.DefaultPercent;
    //    rightslider.value = scene.DefaultPercent;
    //}

    // Extend the unlock if ThalmcHub's locking policy is standard, and notifies the given myo that a user action was
    // recognized.
    //void ExtendUnlockAndNotifyUserAction(ThalmicMyo myo)
    //{
    //    ThalmicHub hub = ThalmicHub.instance;

    //    if (hub.lockingPolicy == LockingPolicy.Standard)
    //    {
    //        myo.Unlock(UnlockType.Timed);
    //    }

    //    myo.NotifyUserAction();
    //}

}
