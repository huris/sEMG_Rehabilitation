using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class ManController : MonoBehaviour
{
    // Start is called before the first frame update
    float Separate = 0;
    float RaisePercent = 0;
    bool israising = false;
    float currenttime = 0;
    float currentraisetime = 0;
    Animator anim;
    public Animation sepleg;
    void Start()
    {
        anim = GetComponent<Animator>();
        anim.SetFloat("separate",0);
    }

    // Update is called once per frame
    void Update()
    {
        currenttime = anim.GetCurrentAnimatorStateInfo(0).normalizedTime;
        currentraisetime = anim.GetCurrentAnimatorStateInfo(1).normalizedTime;
        //Debug.Log(currentraisetime);
        if (Mathf.Abs(Separate - currenttime) <= 0.01)
            anim.SetFloat("separate", 0);
        if (israising&&Mathf.Abs(RaisePercent - currentraisetime) <= 0.01)
            anim.SetFloat("raisespeed", -RaisePercent);
        if(israising&&currentraisetime<=0&&anim.GetFloat("raisespeed")<0)
        {
            israising = false;
            anim.SetBool("israising", israising);
            anim.SetFloat("raisespeed", RaisePercent);
        }    
    }

    public void separateleg(float percent)
    {
        float currenttime = anim.GetCurrentAnimatorStateInfo(0).normalizedTime;
        if (percent > currenttime)
            anim.SetFloat("separate", 1);
        else if (currenttime > percent)
        {
            anim.SetFloat("separate", -1);
        }
        Separate = percent;
    }

    public void SetRaisePer(float percent)
    {
        RaisePercent = percent;
        anim.SetFloat("raisespeed", RaisePercent);
    }

    public void RaiseL()
    {        
        //Debug.Log(RaisePercent);
        israising = true;
        anim.SetBool("israising", israising);
        anim.SetTrigger("raiseL");
    }

    public void RaiseR()
    {       
        israising = true;
        anim.SetBool("israising", israising);
        anim.SetTrigger("raiseR");
    }

    public void RaiseAll()
    {       
        israising = true;
        anim.SetBool("israising", israising);
        anim.SetTrigger("raise");
    }
}
