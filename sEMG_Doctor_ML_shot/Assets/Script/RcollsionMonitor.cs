using System.Collections;
using System.Collections.Generic;
using System.Linq;
using UnityEngine;
using UnityEngine.UI;

public class RcollsionMonitor : MonoBehaviour
{
    private Rigidbody rgd;
    public float force;
    public float wallforce;
    public float footforce;

    public float gravity;
    public float wallgravity;
    public float footgravity;

    public bool willLaunch;

    void OnEnable()
    {
        rgd = GetComponent<Rigidbody>(); //��ȡ�����ϵĸ������
        wallforce = -10f;
        footforce = 15f;
        force = wallforce;

        wallgravity = -3f;
        footgravity = 20f;
        gravity = wallgravity;

        willLaunch = false;
    }

    void Update()
    {
        //float h = Input.GetAxis("Horizontal");//ˮƽ���� ��Ӧ�� ��
        //float v = Input.GetAxis("Vertical"); //��ֱ���� ��Ӧ�� �� 
        ////rgd.AddForce(new Vector3(h, 0, v) * speed);//������ʩ��һ�����Ϳ����˶���,���һ�����򼴿�

        //print(force);

        if (willLaunch)
        {
            int num = DataManager.instance.LsEMGData.Count;
            //if (num > 0 && DataManager.instance.LsEMGData.Last() > 0.4f)
            if (num > 0 && DataManager.instance.LsEMGData.Last() < 0.2f)
            {
                int n = Mathf.Min(7, num);
                while(n > 1)
                {
                    if (DataManager.instance.RsEMGData[num - n] < DataManager.instance.RsEMGData[num - n + 1])
                    {
                        //print(DataManager.instance.RsEMGData[num - n] + " " + DataManager.instance.RsEMGData[num - n + 1]);
                        break;
                    }
                    n--;
                }
                if(n == 1)
                {
                    force = footforce;
                    gravity = footgravity;
                    willLaunch = false;
                }
            }
        }
        else
        {
            //rgd.AddForce(new Vector3(0, 0, force));

            rgd.AddForce(new Vector3(0, gravity, force));
        }
    }

    void OnCollisionEnter(Collision collision) {
        //Debug.Log("Name is " + name);

        if (collision.collider.name == "wall") {
            //rgd.AddForce(new Vector3(0, 0, force));
            force = wallforce;
            gravity = wallgravity;
        }
        else if(collision.collider.name == "footbox")
        {
            willLaunch = true;
        }

    }
}
