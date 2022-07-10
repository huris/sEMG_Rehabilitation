using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;
using System;
using System.IO;
using System.Linq;
using System.Net;
using System.Net.Sockets;
using System.Runtime.Serialization;
using System.Text;
using System.Threading;


public class ManOne : MonoBehaviour
{
    Man rightman;
    Man leftman;
    private float speed;
    private GameObject Canvas;

    public int cs = 1;
    public int plus = 1;
    public float rightValue = 0.0f;

    // 调整脚的转动速度
    public static int FrameMax = 99;
    public static int FrameMin = 0;

    // 通信
    private string message;
    private string end_tag = Encoding.UTF8.GetString(Encoding.UTF8.GetBytes("exit"));
    private Socket client;
    private string host = "127.0.0.1";
    private int port = 10086;
    private byte[] messTmp = new byte[1024];
    public int cnt = 0;

    void Start()
    {
        // 构建一个Socket实例，并连接指定的服务端。这里需要使用IPEndPoint类(ip和端口号的封装)
        client = new Socket(AddressFamily.InterNetwork, SocketType.Stream, ProtocolType.Tcp);

        try
        {
            client.Connect(new IPEndPoint(IPAddress.Parse(host), port));
        }
        catch (Exception e)
        {
            Console.WriteLine(e.Message);
            return;
        }
    }

    // Start is called before the first frame update
    void OnEnable()
    {
        rightman = transform.Find("manright").GetComponent<Man>();
        leftman = transform.Find("manleft").GetComponent<Man>();
        speed = 1;
        cs = 1;
        plus = 1;
        rightValue = 0.0f;

        Canvas = GameObject.Find("Canvas");
    }

    // Update is called once per frame
    void Update()
    {
        
    }

    void FixedUpdate()
    {
        if (cs == FrameMax || cs == FrameMin)
        {
            plus = -plus;
        }
        cs += plus;
        rightValue = 1.0f * cs / (FrameMax - FrameMin + 1);
        ChangeRightLeg(rightValue);

        GetMessage(rightValue);
    }

    void OnDestroy()
    {
        SendOver(true, 0);
        client.Close();
    }

    public void ChangeRightLeg(float percent)
    {
        rightman.ChangeAll(percent);
    }

    public void ChangeLeftLeg(float percent)
    {
        leftman.ChangeAll(percent);
    }

    void GetMessage(float MoveValue)
    {
        client.Receive(messTmp);

        message = Encoding.UTF8.GetString(messTmp);

        SendOver(false, MoveValue);
    }

    void SendOver(bool isExit, float MoveValue)
    {
        byte[] buffer;
        if (isExit)
        {
            // 发一个2说明退出程序
            buffer = Encoding.UTF8.GetBytes("2");
        }
        else
        {
            buffer = Encoding.UTF8.GetBytes(MoveValue.ToString());
        }
        client.Send(buffer);
    }
}
