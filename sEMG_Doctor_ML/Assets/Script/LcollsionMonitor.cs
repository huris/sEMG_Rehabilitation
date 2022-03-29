using System.Collections;
using System.Collections.Generic;
using System.Linq;
using UnityEngine;
using UnityEngine.UI;

public class LcollsionMonitor : MonoBehaviour
{
    private Rigidbody rgd;
    public float force;
    public float wallforce;
    public float footforce;
    public bool willLaunch;

    void OnEnable()
    {
        rgd = GetComponent<Rigidbody>(); //��ȡ�����ϵĸ������
        wallforce = -15f;
        footforce = 20f;
        force = wallforce;
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
            if (num > 0 && DataManager.instance.LsEMGData.Last() > 0.4f)
            {
                int n = Mathf.Min(7, num);
                while(n > 1)
                {
                    if (DataManager.instance.LsEMGData[num - n] > DataManager.instance.LsEMGData[num - n + 1])
                    {
                        //print(DataManager.instance.LsEMGData[num - n] + " " + DataManager.instance.LsEMGData[num - n + 1]);
                        break;
                    }
                    n--;
                }
                if(n == 1)
                {
                    force = footforce;
                    willLaunch = false;
                }
            }
        }else
        {
            rgd.AddForce(new Vector3(0, 0, force));
        }
    }

    void OnCollisionEnter(Collision collision) {
        //Debug.Log("Name is " + name);

        if (collision.collider.name == "wall") {
            //rgd.AddForce(new Vector3(0, 0, force));
            force = wallforce;
        } else if(collision.collider.name == "footbox")
        {
            willLaunch = true;
        }

    }
}
