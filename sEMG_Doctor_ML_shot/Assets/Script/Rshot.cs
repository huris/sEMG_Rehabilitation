using System.Collections;
using System.Collections.Generic;
using System.Linq;
using UnityEngine;
using UnityEngine.UI;

public class Rshot : MonoBehaviour
{
    public Transform shot;

    public int RsEMGNum;

    void OnEnable()
    {

    }

    void Update()
    {

        RsEMGNum = DataManager.instance.RsEMGData.Count;
        if (RsEMGNum > 0)
        {
            if (shot.localPosition.z > DataManager.instance.RsEMGData[RsEMGNum - 1] + 1.36f)
            {
                shot.localPosition = new Vector3(0.215f, 0.094f, DataManager.instance.RsEMGData[RsEMGNum - 1] + 1.36f);

            }
            else if (DataManager.instance.RsEMGData[RsEMGNum - 1] > 0.5)
            {
                shot.localPosition = new Vector3(0.215f, 0.094f, 1.7f);
            }
        }
        
    }
}
