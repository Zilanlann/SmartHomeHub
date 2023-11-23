/****************************************************************************
* �� �� ��: main.c
* ��    ��: ���ɼ�������ʪ��ͨ�����ڷ��͵����ڵ�����������ʾ 9600 8N1
            �й�ʱLED1�������ֵ�ס��������ʱLED1Ϩ��
****************************************************************************/
#include <ioCC2530.h>
#include <string.h>
#include "UART.H" 
#include "DHT11.H" 


#define LED1 P1_0            //����P1.0��ΪLED1���ƶ�
#define LED2 P1_1            //����P1.1��ΪLED2���ƶ�
#define DATA_PIN P0_5        //����P0.5��Ϊ�����������

/****************************************************************************
* ��    ��: InitLed()
* ��    ��: ����LED����Ӧ��IO��
* ��ڲ���: ��
* ���ڲ���: ��
****************************************************************************/
void InitLed(void)
{
    P1DIR |= 0x03;           // P10 P11 Ϊ���
}
/****************************************************************************
* ������ں���
****************************************************************************/
void main(void)
{  
    P0DIR &= ~0x20;          //P0.5����Ϊ����� 
    InitLed();               //����LED����Ӧ��IO��
    uchar temp[3]; 
    uchar humidity[3];   
    uchar strTemp[13]="Temperature:";
    uchar strHumidity[10]="Humidity:";
    Delay_ms(1000);          //���豸�ȶ�
    InitUart();              //���ڳ�ʼ��
    while(1)
    {
        memset(temp, 0, 3);
        memset(humidity, 0, 3);
        if(DATA_PIN == 1)    //���������账�ںڰ���ʱP0.5�ߵ�ƽ,LED1Ϩ��
        {
            LED1 = 0;
            UartSendString("Sunlight:No\n", 12);
        }
        else
        {
            LED1 = 1;       //��⵽����ʱP0.5Ϊ�͵�ƽLED1��
            UartSendString("Sunlight:Yes\n", 13);
        }
        DHT11();             //��ȡ��ʪ��

        //����ʪ�ȵ�ת�����ַ���
        temp[0]=wendu_shi+0x30;
        temp[1]=wendu_ge+0x30;
        humidity[0]=shidu_shi+0x30;
        humidity[1]=shidu_ge+0x30;
        
        //��õ���ʪ��ͨ���������
        UartSendString(strTemp, 12);
        UartSendString(temp, 2);
        UartSendString(" ", 1);
        UartSendString(strHumidity, 9);
        UartSendString(humidity, 2);
        UartSendString("\n", 1);
        
  
        Delay_ms(2000);  //��ʱ��2S��ȡ1�� 
    }
}
