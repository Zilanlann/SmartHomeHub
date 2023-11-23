/****************************************************************************
* 文 件 名: main.c
* 描    述: 将采集到的温湿度通过串口发送到串口调试助手上显示 9600 8N1
            有光时LED1亮，用手挡住光敏电阻时LED1熄灭
****************************************************************************/
#include <ioCC2530.h>
#include <string.h>
#include "UART.H" 
#include "DHT11.H" 


#define LED1 P1_0            //定义P1.0口为LED1控制端
#define LED2 P1_1            //定义P1.1口为LED2控制端
#define DATA_PIN P0_5        //定义P0.5口为传感器输入端

/****************************************************************************
* 名    称: InitLed()
* 功    能: 设置LED灯相应的IO口
* 入口参数: 无
* 出口参数: 无
****************************************************************************/
void InitLed(void)
{
    P1DIR |= 0x03;           // P10 P11 为输出
}
/****************************************************************************
* 程序入口函数
****************************************************************************/
void main(void)
{  
    P0DIR &= ~0x20;          //P0.5定义为输入口 
    InitLed();               //设置LED灯相应的IO口
    uchar temp[3]; 
    uchar humidity[3];   
    uchar strTemp[13]="Temperature:";
    uchar strHumidity[10]="Humidity:";
    Delay_ms(1000);          //让设备稳定
    InitUart();              //串口初始化
    while(1)
    {
        memset(temp, 0, 3);
        memset(humidity, 0, 3);
        if(DATA_PIN == 1)    //当光敏电阻处于黑暗中时P0.5高电平,LED1熄灭
        {
            LED1 = 0;
            UartSendString("Sunlight:No\n", 12);
        }
        else
        {
            LED1 = 1;       //检测到光线时P0.5为低电平LED1亮
            UartSendString("Sunlight:Yes\n", 13);
        }
        DHT11();             //获取温湿度

        //将温湿度的转换成字符串
        temp[0]=wendu_shi+0x30;
        temp[1]=wendu_ge+0x30;
        humidity[0]=shidu_shi+0x30;
        humidity[1]=shidu_ge+0x30;
        
        //获得的温湿度通过串口输出
        UartSendString(strTemp, 12);
        UartSendString(temp, 2);
        UartSendString(" ", 1);
        UartSendString(strHumidity, 9);
        UartSendString(humidity, 2);
        UartSendString("\n", 1);
        
  
        Delay_ms(2000);  //延时，2S读取1次 
    }
}
