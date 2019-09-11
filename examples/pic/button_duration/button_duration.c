/*
 * File:   button_duration.c
 * Author: seitzaj, modified by ZJE to remove UART and just logic high
 *
 * Created on October 31, 2018, 2:51 PM
 * Last revised July 11, 2019
 */

#include <xc.h>

// CONFIG1
//#pragma config FOSC = INTRC_NOCLKOUT// Oscillator Selection bits (INTOSCIO oscillator: I/O function on RA6/OSC2/CLKOUT pin, I/O function on RA7/OSC1/CLKIN)
//#pragma config FOSC = EC        // Oscillator Selection bits (EC: I/O function on RA6/OSC2/CLKOUT pin, CLKIN on RA7/OSC1/CLKIN)
#pragma config FOSC = HS        // Oscillator Selection bits (HS oscillator: High-speed crystal/resonator on RA6/OSC2/CLKOUT and RA7/OSC1/CLKIN)
#pragma config WDTE = OFF       // Watchdog Timer Enable bit (WDT disabled and can be enabled by SWDTEN bit of the WDTCON register)
#pragma config PWRTE = OFF      // Power-up Timer Enable bit (PWRT disabled)
#pragma config MCLRE = ON       // RE3/MCLR pin function select bit (RE3/MCLR pin function is MCLR)
#pragma config CP = OFF         // Code Protection bit (Program memory code protection is disabled)
#pragma config CPD = OFF        // Data Code Protection bit (Data memory code protection is disabled)
#pragma config BOREN = OFF      // Brown Out Reset Selection bits (BOR disabled)
#pragma config IESO = OFF       // Internal External Switchover bit (Internal/External Switchover mode is disabled)
#pragma config FCMEN = OFF      // Fail-Safe Clock Monitor Enabled bit (Fail-Safe Clock Monitor is disabled)
#pragma config LVP = OFF        // Low Voltage Programming Enable bit (RB3 pin has digital I/O, HV on MCLR must be used for programming)

// CONFIG2
#pragma config BOR4V = BOR21V   // Brown-out Reset Selection bit (Brown-out Reset set to 2.1V)
#pragma config WRT = OFF        // Flash Program Memory Self Write Enable bits (Write protection off)

// Function prototypes
void __interrupt() interrupt_handler(void);
void Timer_CCP_init(void);

unsigned char counter = 0;
unsigned char debounce_ms = 68;//REMEMBER: *2 if using FOSC = HS
unsigned int period;

void main(void) {
    // Disable analog inputs
    ANSEL = 0;
    ANSELH = 0;
    
    // Enable pull-up resistors on PORTB
    TRISB0 = 0x01; // Set RB0 as input
    nRBPU = 0; 
    // Enable PORTB interrupt-on-change
    IOCB0 = 1;
    RBIF = 0;
    RBIE = 1;
    
    TRISA = 0x00; // RA0, RA1, RA2 as output
    TRISC6 = 0;
    RC6 = 0;
    RA0 = 0; RA1 = 0; RA2 = 0;
    
    period = ((debounce_ms * 100) / 8) * 10;
    Timer_CCP_init();
    
    GIE = 1;
    
    while(1);
    
}


void Timer_CCP_init(void)
{
	TMR1GE=0;   TMR1ON = 1; 		//Enable TIMER1 (See Fig. 6-1 TIMER1 Block Diagram in PIC16F887 Data Sheet)
	TMR1CS = 0;  					//Select internal clock whose frequency is Fosc/4, where Fosc = 4 MHz
	T1CKPS1 = 1; T1CKPS0 = 1; 		//Set prescale to divide by 8 yielding a clock tick period of 8 microseconds
    
	CCP1M3 = 0;CCP1M2 = 0;CCP1M1 = 1;CCP1M0 = 0; 	// Set to Compare Mode, toggle on match
	TRISC2 = 0;                     //Make CCP1 pin an output.
	
	CCP1IF = 0;
	PEIE = 1;					//Enable all peripheral interrupts 
}

void __interrupt() interrupt_handler(void){
    if ((CCP1IE == 1) && (CCP1IF == 1)){
        //RA2 ^= 1;
        RA0 = 0;
        
        if (RB0 == 0)
        {
            RC6 = 1;
        }
        
        RBIE = 1;
        RBIF = 0;
        CCP1IE = 0;
        CCP1IF = 0;
    }
    
    if ((RBIE == 1) && (RBIF == 1)){ // Check for interrupt
        //RA1 ^= 1;
        RBIE = 0;
        RA0 = 1;
        
        CCPR1 = TMR1 + period;
        CCP1IE = 1;
        CCP1IF = 0;
        
        RBIF = 0;  // Clear interrupt
    }

}
