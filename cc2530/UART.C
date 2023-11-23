#include <ioCC2530.h>
#include "UART.H" 

// ���ڳ�ʼ������     
void InitUart()
{
    CLKCONCMD &= ~0x40;      // ����ϵͳʱ��ԴΪ 32MHZ����
    while(CLKCONSTA & 0x40); // �ȴ������ȶ� 
    CLKCONCMD &= ~0x47;      // ����ϵͳ��ʱ��Ƶ��Ϊ 32MHZ
    
    PERCFG = 0x00;           //λ��1 P0�� 
    P0SEL = 0x0c;            //P0_2,P0_3��������,�ڶ����� 
    P2DIR &= ~0xC0;          //P0 ������ΪUART0 �����ȼ�
    
    U0CSR |= 0x80;           //UART ��ʽ 
    U0GCR |= 8;             //U0GCR��U0BAUD���     
    U0BAUD |= 59;           // ��������Ϊ9600
    UTX0IF = 0;              //UART0 TX �жϱ�־��ʼ��λ0 
    
}

//���ڷ��ͺ���    
void UartSendString(unsigned char *Data, int len) 
{
    int j; 
    for(j=0;j<len;j++) 
    { 
        U0DBUF = *Data++; 
        while(UTX0IF == 0); 
        UTX0IF = 0; 
    } 
    
}