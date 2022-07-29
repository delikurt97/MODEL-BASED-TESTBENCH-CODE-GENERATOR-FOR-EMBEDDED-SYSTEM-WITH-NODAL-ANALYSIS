
from distutils.log import error
from sqlite3 import connect
from tkinter import W
import system_clock_config

import shutil 
import os
import PyQt5
import array as arr
import dictionary_of_pin
import numpy as np
uart_direction=[0,0,0,0,0]
uart_baud=[0,0,0,0,0]
uart_transmit_data=["","","","",""]
uart_receive_data=["","","","",""]
uart_cont_trans=["","","","",""]
uart_cont_receive=["","","","",""]
uart_pin=[["UART4", "A","1","C","10","huart4"],["UART5","C","12","D","2","huart5"],["USART2","A","2","A","3","huart2"],["USART3","B","11","D","8","huart3"],["USART6","C","6","C","7","huart6"],["USART1","B","6","B","7","huart1"]]
c=[["TIM2","2","A","15"],["TIM3","3","A","6"],["TIM4","4","D","12"],["TIM5","5","A","0"]]
a=[["E","12"],["E","13"],["E","14"],["E","15"],["E","11"]]
b=[["B","1"],["B","2"],["B","3"]]
dac1up_range=[]
dac2up_range=[]
dac1low_range=[]
dac2low_range=[]
sumreason=[]
sumresult=[]
errorsum=[]
frequency=[]
duty=[]


def GPIO_In(Number_of_GPIO_IN):
    jkjkj=Number_of_GPIO_IN
    klklk=Number_of_GPIO_IN
    mkmk=Number_of_GPIO_IN
    with open("main.c", "r") as in_file:
        buf = in_file.readlines()

    with open("main.c", "w") as out_file:
        for line in buf:
            if line == "//Configure GPIO\n":
                line = line + f"__HAL_RCC_GPIO{b[0][0]}_CLK_ENABLE();\n"
                while jkjkj>0:
                    line = line + f"GPIO_InitStruct.Pin = GPIO_PIN_{b[Number_of_GPIO_IN-jkjkj][1]};\n"
                    line = line + "GPIO_InitStruct.Mode = GPIO_MODE_INPUT;\n"
                    line = line + "GPIO_InitStruct.Pull = GPIO_NOPULL;\n"
                    line = line + f"HAL_GPIO_Init(GPIO{b[0][0]}, &GPIO_InitStruct);\n"
                    jkjkj=jkjkj-1
            if line== "/* Private variables */\n":
                while mkmk>0:
                    line=line+f"int errorIn{Number_of_GPIO_IN-mkmk+1};\n"
                    mkmk=mkmk-1

            if line == "//Before the infinite loop\n":
                while klklk>0:
                    
                    line = line + f"//Begin of GPIO_IN{Number_of_GPIO_IN-klklk+1}\n"
                    line = line + f"if(HAL_GPIO_ReadPin(GPIO{b[Number_of_GPIO_IN-klklk][0]}, GPIO_PIN_{b[Number_of_GPIO_IN-klklk][1]}))\n"
                    line = line + "{\n"
                    line = line + f"errorIn{Number_of_GPIO_IN-klklk+1}=0;\n"
                    line = line + "}\n"
                    line = line + "else\n"
                    line = line + "{\n"
                    line = line + f"errorIn{Number_of_GPIO_IN-klklk+1}++;\n"
                    line = line + "}\n"
                    line = line + f"//End of GPIO_IN{Number_of_GPIO_IN-klklk+1}\n"
                    klklk=klklk-1
            out_file.write(line) 

def GPIO_OUT(Number_of_GPIO_OUT):
    jljl=Number_of_GPIO_OUT
    jkjkl=Number_of_GPIO_OUT
    with open("main.c", "r") as in_file:
        buf = in_file.readlines()

    with open("main.c", "w") as out_file:
        for line in buf:
            if line == "//Configure GPIO\n":
                line = line + f"__HAL_RCC_GPIO{a[0][0]}_CLK_ENABLE();\n"
                while jljl>0:
                   
                    line = line + f"GPIO_InitStruct.Pin = GPIO_PIN_{a[Number_of_GPIO_OUT-jljl][1]};\n"
                    line = line + "GPIO_InitStruct.Mode = GPIO_MODE_OUTPUT_PP;\n"
                    line = line + "GPIO_InitStruct.Pull = GPIO_NOPULL;\n"
                    line = line + "GPIO_InitStruct.Speed = GPIO_SPEED_FREQ_LOW;\n"
                    line = line + f"HAL_GPIO_Init(GPIO{a[0][0]}, &GPIO_InitStruct);\n"
                    jljl=jljl-1
            if line == "//Before the infinite loop\n":
                while jkjkl>0:
                    line = line + f"//Begin of GPIO_OUT{Number_of_GPIO_OUT-jkjkl+1}\n"
                    line = line + f"HAL_GPIO_WritePin(GPIO{a[0][0]}, GPIO_PIN_{a[Number_of_GPIO_OUT-jkjkl][1]}, GPIO_PIN_SET);\n"
                    line = line + f"//End of GPIO_OUT{Number_of_GPIO_OUT-jkjkl+1}\n"
                    jkjkl=jkjkl-1
            out_file.write(line) 



                


def DAC_Checker(number_of_ADC): #Bu isimler kafamı karıştırıyo aq

    if number_of_ADC>0  :      
        aa=number_of_ADC
        with open("stm32f4xx_hal_conf.h", "r") as in_file:
            buf = in_file.readlines()

        with open("stm32f4xx_hal_conf.h", "w") as out_file:
            for line in buf:
                if line == "/* #define HAL_DAC_MODULE_ENABLED   */\n":
                    line = "#define HAL_DAC_MODULE_ENABLED\n"
                out_file.write(line)

        with open("stm32f4xx_hal_msp.c", "r") as in_file:
            buf = in_file.readlines()

        with open("stm32f4xx_hal_msp.c", "w") as out_file:
            for line in buf:
                if aa==2:
                    if line == "/* USER CODE BEGIN 1 */\n":
                        line = line +"void HAL_DAC_MspInit(DAC_HandleTypeDef* hdac)\n"
                        line = line +"{\n"
                        line = line +"GPIO_InitTypeDef GPIO_InitStruct = {0};\n"
                        line = line +" if(hdac->Instance==DAC)\n"
                        line = line +"  {\n"
                        line = line +"   __HAL_RCC_DAC_CLK_ENABLE();\n"
                        line = line +f"  __HAL_RCC_GPIO{dictionary_of_pin.pa4['GPIO']}_CLK_ENABLE();\n"
                        line = line +" /**DAC GPIO Configuration\n"
                        line = line +"  PA4     ------> DAC_OUT1\n"
                        line = line +"  PA5     ------> DAC_OUT2\n"
                        line = line +"    */\n"
                        line = line +f"GPIO_InitStruct.Pin = GPIO_PIN_{dictionary_of_pin.pa4['Pin_Number']}|GPIO_PIN_{dictionary_of_pin.pa5['Pin_Number']};\n"
                        line = line +"GPIO_InitStruct.Mode = GPIO_MODE_ANALOG;\n"
                        line = line +"GPIO_InitStruct.Pull = GPIO_NOPULL;\n"
                        line = line +f"    HAL_GPIO_Init(GPIO{dictionary_of_pin.pa4['GPIO']}, &GPIO_InitStruct);\n"
                        line = line +"  }\n"
                        line = line +"}\n"
                        line = line +"void HAL_DAC_MspDeInit(DAC_HandleTypeDef* hdac)\n"
                        line = line +"{\n"
                        line=line+" if(hdac->Instance==DAC){\n"
                        line = line +"    __HAL_RCC_DAC_CLK_DISABLE();\n"
                        line = line +" /**DAC GPIO Configuration\n"
                        line = line +"  PA4     ------> DAC_OUT1\n"
                        line = line +"  PA5     ------> DAC_OUT2\n"
                        line = line +"    */\n"
                        line = line +f"    HAL_GPIO_DeInit(GPIO{dictionary_of_pin.pa4['GPIO']}, GPIO_PIN_{dictionary_of_pin.pa4['Pin_Number']}|GPIO_PIN_{dictionary_of_pin.pa5['Pin_Number']});\n"
                        line=line+" }\n"
                        line=line+" }\n"

                elif aa==1 and dictionary_of_pin.pa4['Availability']=='Avaible':
                    if line == "/* USER CODE BEGIN 1 */\n":
                        line = line +"void HAL_DAC_MspInit(DAC_HandleTypeDef* hdac)\n"
                        line = line +"{\n"
                        line = line +"GPIO_InitTypeDef GPIO_InitStruct = {0};\n"
                        line = line +" if(hdac->Instance==DAC)\n"
                        line = line +"  {\n"
                        line = line +"   __HAL_RCC_DAC_CLK_ENABLE();\n"
                        line = line +f"  __HAL_RCC_GPIO{dictionary_of_pin.pa4['GPIO']}_CLK_ENABLE();\n"
                        line = line +" /**DAC GPIO Configuration\n"
                        line = line +"  PA4     ------> DAC_OUT1\n"
                        line = line +"    */\n"
                        line = line +f"GPIO_InitStruct.Pin = GPIO_PIN_{dictionary_of_pin.pa4['Pin_Number']};\n"
                        line = line +"GPIO_InitStruct.Mode = GPIO_MODE_ANALOG;\n"
                        line = line +"GPIO_InitStruct.Pull = GPIO_NOPULL;\n"
                        line = line +f"    HAL_GPIO_Init(GPIO{dictionary_of_pin.pa4['GPIO']}, &GPIO_InitStruct);\n"
                        line = line +"  }\n"
                        line = line +"}\n"
                        line = line +"void HAL_DAC_MspDeInit(DAC_HandleTypeDef* hdac)\n"
                        line = line +"{\n"
                        line=line+" if(hdac->Instance==DAC){\n"
                        line = line +"    __HAL_RCC_DAC_CLK_DISABLE();\n"
                        line = line +" /**DAC GPIO Configuration\n"
                        line = line +"  PA4     ------> DAC_OUT1\n"
                        line = line +"    */\n"
                        line = line +f"    HAL_GPIO_DeInit(GPIO{dictionary_of_pin.pa4['GPIO']}, GPIO_PIN_{dictionary_of_pin.pa4['Pin_Number']});\n"
                        line=line+" }\n"
                        line=line+" }\n"
                elif aa==1 and dictionary_of_pin.pa5['Availability']=='Avaible':
                    if line == "/* USER CODE BEGIN 1 */\n":
                        line = line +"void HAL_DAC_MspInit(DAC_HandleTypeDef* hdac)\n"
                        line = line +"{\n"
                        line = line +"GPIO_InitTypeDef GPIO_InitStruct = {0};\n"
                        line = line +" if(hdac->Instance==DAC)\n"
                        line = line +"  {\n"
                        line = line +"   __HAL_RCC_DAC_CLK_ENABLE();\n"
                        line = line +f"  __HAL_RCC_GPIO{dictionary_of_pin.pa5['GPIO']}_CLK_ENABLE();\n"
                        line = line +" /**DAC GPIO Configuration\n"
                        line = line +"  PA5     ------> DAC_OUT2\n"
                        line = line +"    */\n"
                        line = line +f"GPIO_InitStruct.Pin = GPIO_PIN_{dictionary_of_pin.pa5['Pin_Number']};\n"
                        line = line +"GPIO_InitStruct.Mode = GPIO_MODE_ANALOG;\n"
                        line = line +"GPIO_InitStruct.Pull = GPIO_NOPULL;\n"
                        line = line +f"    HAL_GPIO_Init(GPIO{dictionary_of_pin.pa5['GPIO']}, &GPIO_InitStruct);\n"
                        line = line +"  }\n"
                        line = line +"}\n"
                        line = line +"void HAL_DAC_MspDeInit(DAC_HandleTypeDef* hdac)\n"
                        line = line +"{\n"
                        line=line+" if(hdac->Instance==DAC)\n{\n"
                        line = line +"    __HAL_RCC_DAC_CLK_DISABLE();\n"
                        line = line +" /**DAC GPIO Configuration\n"
                        line = line +"  PA5     ------> DAC_OUT2\n"
                        line = line +"    */\n"
                        line = line +f"    HAL_GPIO_DeInit(GPIO{dictionary_of_pin.pa5['GPIO']}, GPIO_PIN_{dictionary_of_pin.pa5['Pin_Number']});\n"
                        line=line+" }\n"
                        line=line+" }\n"
                out_file.write(line)

        with open("main.c", "r") as in_file:
            buf = in_file.readlines()

        with open("main.c", "w") as out_file:
            for line in buf:
                if line == "/* Private variables */\n":
                    line = line +" DAC_HandleTypeDef hdac;\n"
                if line == "//Function prototype area\n":
                    line = line +"static void MX_DAC_Init(void);\n"
                if line == "//Function calling area\n":
                    line = line +"  MX_DAC_Init();\n"
                if aa==2:
                    if line == "/* USER CODE  */\n":
                        line = line +"HAL_DAC_Start(&hdac, DAC_CHANNEL_1);\n"
                        line = line +"HAL_DAC_Start(&hdac, DAC_CHANNEL_2);\n"
                        
                elif aa==1 and dictionary_of_pin.pa4['Availability']=='Avaible':
                    if line == "/* USER CODE  */\n":
                        line = line +"HAL_DAC_Start(&hdac, DAC_CHANNEL_1);\n"
                    
                elif aa==1 and dictionary_of_pin.pa5['Availability']=='Avaible':
                    if line == "/* USER CODE  */\n":
                        
                        line = line +"HAL_DAC_Start(&hdac, DAC_CHANNEL_2);\n" 
                if aa==2:
                    if line == "//Function area\n":
                        line = line +"static void MX_DAC_Init(void)\n"
                        line = line +"{\n"
                        line=line+"   DAC_ChannelConfTypeDef sConfig = {0};\n"
                        line = line +"    hdac.Instance = DAC;\n"
                        line = line +"   if (HAL_DAC_Init(&hdac) != HAL_OK)\n"
                        line = line +"   {\n"
                        line = line +"    Error_Handler();\n"
                        line = line +"     }\n"
                        line=line+"     sConfig.DAC_Trigger = DAC_TRIGGER_NONE;\n"
                        line = line +"  sConfig.DAC_OutputBuffer = DAC_OUTPUTBUFFER_ENABLE;\n"
                        line = line +"   if (HAL_DAC_ConfigChannel(&hdac, &sConfig, DAC_CHANNEL_1) != HAL_OK)\n"
                        line = line +"   {\n"
                        line = line +"    Error_Handler();\n"
                        line = line +"     }\n"
                        line = line +"    if (HAL_DAC_ConfigChannel(&hdac, &sConfig, DAC_CHANNEL_2) != HAL_OK)\n"
                        line = line +"   {\n"
                        line = line +"    Error_Handler();\n"
                        line = line +"     }\n"
                        line = line +"     }\n"
                elif aa==1 and dictionary_of_pin.pa4['Availability']=='Avaible':
                    if line == "//Function area\n":
                        line = line +"static void MX_DAC_Init(void)\n"
                        line = line +"{\n"
                        line=line+"   DAC_ChannelConfTypeDef sConfig = {0};\n"
                        line = line +"    hdac.Instance = DAC;\n"
                        line = line +"   if (HAL_DAC_Init(&hdac) != HAL_OK)\n"
                        line = line +"   {\n"
                        line = line +"    Error_Handler();\n"
                        line = line +"     }\n"
                        line=line+"     sConfig.DAC_Trigger = DAC_TRIGGER_NONE;\n"
                        line = line +"  sConfig.DAC_OutputBuffer = DAC_OUTPUTBUFFER_ENABLE;\n"
                        line = line +"   if (HAL_DAC_ConfigChannel(&hdac, &sConfig, DAC_CHANNEL_1) != HAL_OK)\n"
                        line = line +"   {\n"
                        line = line +"    Error_Handler();\n"
                        line = line +"     }\n"
                        line = line +"     }\n"
                elif aa==1 and dictionary_of_pin.pa5['Availability']=='Avaible':
                    if line == "//Function area\n":
                        line = line +"static void MX_DAC_Init(void)\n"
                        line = line +"{\n"
                        line=line+"   DAC_ChannelConfTypeDef sConfig = {0};\n"
                        line = line +"    hdac.Instance = DAC;\n"
                        line = line +"   if (HAL_DAC_Init(&hdac) != HAL_OK)\n"
                        line = line +"   {\n"
                        line = line +"    Error_Handler();\n"
                        line = line +"     }\n"
                        line=line+"     sConfig.DAC_Trigger = DAC_TRIGGER_NONE;\n"
                        line = line +"  sConfig.DAC_OutputBuffer = DAC_OUTPUTBUFFER_ENABLE;\n"
                        line = line +"   if (HAL_DAC_ConfigChannel(&hdac, &sConfig, DAC_CHANNEL_2) != HAL_OK)\n"
                        line = line +"   {\n"
                        line = line +"    Error_Handler();\n"
                        line = line +"     }\n"
                        line = line +"     }\n"

                out_file.write(line)               
        if aa==2:                
            x=int(input("How many ranges exist for DAC1:"))
            y=int(input("How many ranges exist for DAC2:"))
            dac1range=x
            dac2range=y
            sa=x
            da=y
            sad=x
            das=y
            rangedac1_upper_bound=np.zeros(x)
            rangedac1_lower_bound=np.zeros(x)
            rangedac2_upper_bound=np.zeros(y)
            rangedac2_lower_bound=np.zeros(y)
            
            while sa>0:
                rangedac1_upper_bound[x-sa]=float(input(f"{x-sa+1}. upper bound of range for ADC1:::"))
                rangedac1_lower_bound[x-sa]=float(input(f"{x-sa+1}. lower bound of range for ADC1:::"))
                dac1up_range.append(rangedac1_upper_bound[x-sa])
                dac1low_range.append(rangedac1_lower_bound[x-sa])

                sa-=1
            while da>0:
                rangedac2_upper_bound[y-da]=float(input(f"{y-da+1}. upper bound of range for ADC2:::"))
                rangedac2_lower_bound[y-da]=float(input(f"{y-da+1}. lower bound of range for ADC2:::"))
                dac2up_range.append(rangedac2_upper_bound[y-da])
                dac2low_range.append(rangedac2_lower_bound[y-da])
                da-=1
            rangedac1_lower_boundV=((rangedac1_lower_bound*4095)/3.3).astype(int)
            rangedac1_upper_boundV=((rangedac1_upper_bound*4095)/3.3).astype(int)
            rangedac2_lower_boundV=((rangedac2_lower_bound*4095)/3.3).astype(int)
            rangedac2_upper_boundV=((rangedac2_upper_bound*4095)/3.3).astype(int)
            
            with open("main.c", "r") as in_file:
                buf = in_file.readlines()

            with open("main.c", "w") as out_file:
                for line in buf:
                    if line=="/* Private user code */\n":
                        line = line + "uint32_t DAC1_voltage=0;\n"
                        line = line + "uint32_t DAC2_voltage=0;\n"

                    if line == "//Inside of the infinite loop in main function\n":
                        while sad>0:   
                            akkk=(rangedac1_lower_boundV[x-sad]+rangedac1_upper_boundV[x-sad])/2 
                            line = line +f" //Begin of {x-sad+1}. DAC1 interval\n"    
                            line = line +f" DAC1_voltage={akkk};\n"
                       
                            line = line +" HAL_DAC_SetValue(&hdac, DAC_CHANNEL_1, DAC_ALIGN_12B_R, DAC1_voltage);\n"
                            
                            
                            line = line +" HAL_Delay(1000);\n"
                            line = line +f"//End of DAC1-{rangedac1_upper_bound[x-sad]},{rangedac1_lower_bound[x-sad]}\n"
                            sad-=1
                        while das>0:    
                            abbb=(rangedac2_lower_boundV[y-das] + rangedac2_lower_boundV[y-das])/2     
                            line = line +f" //Begin of {y-das+1}. DAC2 interval\n"
                            line = line +f" DAC2_voltage={abbb};\n"
                            
                            line = line +" HAL_DAC_SetValue(&hdac, DAC_CHANNEL_2, DAC_ALIGN_12B_R, DAC2_voltage);\n"
                            line = line +" HAL_Delay(1);\n"
                            
                            line = line +" HAL_Delay(1000);\n"
                            line = line +f"//End of DAC2-{rangedac2_upper_bound[y-das]},{rangedac2_lower_bound[y-das]}\n"
                            das-=1
                    out_file.write(line) 
                    

        if aa==1 and dictionary_of_pin.pa4['Availability']=='Avaible':

            x=int(input("How many ranges exist for DAC1:"))
            print(x)
            dac1range=x
            sa=x
            sad=x
            rangedac1_upper_bound=np.zeros(x)
            rangedac1_lower_bound=np.zeros(x)
            while sa>0:
                rangedac1_upper_bound[x-sa]=float(input(f"{x-sa+1}. upper bound of range for ADC1:::"))
                rangedac1_lower_bound[x-sa]=float(input(f"{x-sa+1}. lower bound of range for ADC1:::"))
                dac1up_range.append(rangedac1_upper_bound[x-sa])
                dac1low_range.append(rangedac1_lower_bound[x-sa])
                sa-=1
            rangedac1_lower_boundV=((rangedac1_lower_bound*4095)/3.3).astype(int)
            rangedac1_upper_boundV=((rangedac1_upper_bound*4095)/3.3).astype(int)

            with open("main.c", "r") as in_file:
                buf = in_file.readlines()

            with open("main.c", "w") as out_file:
                for line in buf:
                    if line=="/* Private user code */\n":
                        line = line + "uint32_t DAC1_voltage=0;\n"

                    if line == "//Inside of the infinite loop in main function\n":
                        while sad>0:    
                            akkk=(rangedac1_lower_boundV[x-sad]+rangedac1_upper_boundV[x-sad])/2
                            line = line +f" //Begin of {x-sad+1}. DAC1 interval\n"    
                            line = line +f" DAC1_voltage={akkk};\n"
                    
                            line = line +" HAL_DAC_SetValue(&hdac, DAC_CHANNEL_1, DAC_ALIGN_12B_R, DAC1_voltage);\n"
                            
                            
                            line = line +" HAL_Delay(1000);\n"
                            line = line +f"//End of DAC1-{rangedac1_upper_bound[x-sad]},{rangedac1_lower_bound[x-sad]}\n"
                            sad-=1
                    out_file.write(line) 

        elif aa==1 and dictionary_of_pin.pa5['Availability']=='Avaible':
            y=int(input("How many ranges exist for DAC2:"))
            dac2range=y
            rangedac2_upper_bound=np.zeros(y)
            rangedac2_lower_bound=np.zeros(y)
            da=y
            das=y
            while da>0:
                rangedac2_upper_bound[y-da]=float(input(f"{y-da+1}. upper bound of range for ADC2:::"))
                rangedac2_lower_bound[y-da]=float(input(f"{y-da+1}. lower bound of range for ADC2:::"))
                dac2up_range.append(rangedac2_upper_bound[y-da])
                dac2low_range.append(rangedac2_lower_bound[y-da])
                da-=1
            rangedac2_lower_boundV=((rangedac2_lower_bound*4095)/3.3).astype(int)
            rangedac2_upper_boundV=((rangedac2_upper_bound*4095)/3.3).astype(int)

            with open("main.c", "r") as in_file:
                buf = in_file.readlines()

            with open("main.c", "w") as out_file:
                for line in buf:
                    if line=="/* Private user code */\n":
                        line = line + "uint32_t DAC2_voltage=0;\n"
                    if line == "//Inside of the infinite loop in main function\n":
                        while das>0:      
                            abbb=(rangedac2_lower_boundV[y-das] + rangedac2_lower_boundV[y-das])/2
                            line = line +f" //Begin of {y-das+1}. DAC2 interval\n"   
                            line = line +f" DAC2_voltage={abbb};\n"
                            line = line +" do{\n"
                            line = line +" e++;\n"
                            line = line +" HAL_DAC_SetValue(&hdac, DAC_CHANNEL_2, DAC_ALIGN_12B_R, e);\n"
                            line = line +" HAL_Delay(1);\n"
                            line = line +" }\n"
                            line = line +f" while(e<{rangedac2_upper_boundV[y-das]});\n"
                            line = line +" HAL_Delay(1000);\n"
                            line = line +f"//End of DAC2-{rangedac2_upper_bound[y-das]},{rangedac2_lower_bound[y-das]}\n"
                            das-=1
                    out_file.write(line) 

def UART_node(uart_node_number):

    
    
    aa=uart_node_number
    bb=uart_node_number
    cc=uart_node_number
    dd=uart_node_number
    ee=uart_node_number
    ff=uart_node_number
    gg=uart_node_number
    hh=uart_node_number
    uu=uart_node_number
            
    with open("stm32f4xx_hal_conf.h", "r") as in_file:
        buf = in_file.readlines()

    with open("stm32f4xx_hal_conf.h", "w") as out_file:
        for line in buf:
            if line == "/* #define HAL_UART_MODULE_ENABLED   */\n":
                line = "#define HAL_UART_MODULE_ENABLED\n"
            out_file.write(line)
    with open("stm32f4xx_hal_msp.c", "r") as in_file:
        buf = in_file.readlines()

    with open("stm32f4xx_hal_msp.c", "w") as out_file:
        for line in buf:
            if line ==  "/* USER CODE BEGIN 1 */\n":
                line = line + "void HAL_UART_MspInit(UART_HandleTypeDef* huart){\n"

                line = line + "GPIO_InitTypeDef GPIO_InitStruct = {0};\n"
                line = line + f"if(huart->Instance=={uart_pin[uart_node_number-aa][0]})\n"
                line = line + "{\n"
                line = line + f"__HAL_RCC_{uart_pin[uart_node_number-aa][0]}_CLK_ENABLE();\n"

                line = line + f"__HAL_RCC_GPIO{uart_pin[uart_node_number-aa][1]}_CLK_ENABLE();\n"
                if uart_pin[uart_node_number-aa][1] != uart_pin[uart_node_number-aa][3]:
                    line = line + f"__HAL_RCC_GPIO{uart_pin[uart_node_number-aa][3]}_CLK_ENABLE();\n"

                line = line + f"GPIO_InitStruct.Pin = GPIO_PIN_{uart_pin[uart_node_number-aa][2]};\n"
                line = line + "GPIO_InitStruct.Mode = GPIO_MODE_AF_PP;\n"
                line = line + "GPIO_InitStruct.Pull = GPIO_NOPULL;\n"
                line = line + "GPIO_InitStruct.Speed = GPIO_SPEED_FREQ_VERY_HIGH;\n"
                line = line + f"GPIO_InitStruct.Alternate = GPIO_AF8_{uart_pin[uart_node_number-aa][0]};\n"
                line = line + f"HAL_GPIO_Init(GPIO{uart_pin[uart_node_number-aa][1]}, &GPIO_InitStruct);\n"

                line = line + f"GPIO_InitStruct.Pin = GPIO_PIN_{uart_pin[uart_node_number-aa][4]};\n"
                line = line + "GPIO_InitStruct.Mode = GPIO_MODE_AF_PP;\n"
                line = line + "GPIO_InitStruct.Pull = GPIO_NOPULL;\n"
                line = line + "GPIO_InitStruct.Speed = GPIO_SPEED_FREQ_VERY_HIGH;\n"
                line = line + f"GPIO_InitStruct.Alternate = GPIO_AF8_{uart_pin[uart_node_number-aa][0]};\n"
                line = line + f"HAL_GPIO_Init(GPIO{uart_pin[uart_node_number-aa][3]}, &GPIO_InitStruct);\n"
                line = line + "}\n"
                aa=aa-1
                if aa>=1:
                    while aa>0:
                        line =line + f"else if(huart->Instance=={uart_pin[uart_node_number-aa][0]})\n"
                        line =line + " {\n"
                        line =line + f" __HAL_RCC_{uart_pin[uart_node_number-aa][0]}_CLK_ENABLE();\n"
                        line = line + f"__HAL_RCC_GPIO{uart_pin[uart_node_number-aa][1]}_CLK_ENABLE();\n"
                        if uart_pin[uart_node_number-aa][1] != uart_pin[uart_node_number-aa][3]:
                            line = line + f"__HAL_RCC_GPIO{uart_pin[uart_node_number-aa][3]}_CLK_ENABLE();\n"
                        line = line + f"GPIO_InitStruct.Pin = GPIO_PIN_{uart_pin[uart_node_number-aa][2]};\n"
                        
                        line = line + "GPIO_InitStruct.Mode = GPIO_MODE_AF_PP;\n"
                        line = line + "GPIO_InitStruct.Pull = GPIO_NOPULL;\n"
                        line = line + "GPIO_InitStruct.Speed = GPIO_SPEED_FREQ_VERY_HIGH;\n"
                        if uart_node_number-aa<=1 or uart_node_number-aa==5:
                            line = line + f"GPIO_InitStruct.Alternate = GPIO_AF8_{uart_pin[uart_node_number-aa][0]};\n"
                        else:
                            line = line + f"GPIO_InitStruct.Alternate = GPIO_AF7_{uart_pin[uart_node_number-aa][0]};\n"

                        line = line + f"HAL_GPIO_Init(GPIO{uart_pin[uart_node_number-aa][1]}, &GPIO_InitStruct);\n"

                        line = line + f"GPIO_InitStruct.Pin = GPIO_PIN_{uart_pin[uart_node_number-aa][4]};\n"
                        line = line + "GPIO_InitStruct.Mode = GPIO_MODE_AF_PP;\n"
                        line = line + "GPIO_InitStruct.Pull = GPIO_NOPULL;\n"
                        line = line + "GPIO_InitStruct.Speed = GPIO_SPEED_FREQ_VERY_HIGH;\n"
                        if uart_node_number-aa<=1 or uart_node_number-aa==5:
                            line = line + f"GPIO_InitStruct.Alternate = GPIO_AF8_{uart_pin[uart_node_number-aa][0]};\n"
                        else:
                            line = line + f"GPIO_InitStruct.Alternate = GPIO_AF7_{uart_pin[uart_node_number-aa][0]};\n"
                        line = line + f"HAL_GPIO_Init(GPIO{uart_pin[uart_node_number-aa][3]}, &GPIO_InitStruct);\n"
                        line = line + "}\n"

                        aa=aa-1
                line = line + "}\n"


                line = line + " void HAL_UART_MspDeInit(UART_HandleTypeDef* huart){\n "
                line = line + f" if(huart->Instance=={uart_pin[uart_node_number-bb][0]})\n "
                line = line + " {\n "
                line = line + f" __HAL_RCC_{uart_pin[uart_node_number-bb][0]}_CLK_DISABLE();\n "
                line = line + f" HAL_GPIO_DeInit(GPIO{uart_pin[uart_node_number-bb][1]}, GPIO_PIN_{uart_pin[uart_node_number-bb][2]});\n "
                line = line + f" HAL_GPIO_DeInit(GPIO{uart_pin[uart_node_number-bb][3]}, GPIO_PIN_{uart_pin[uart_node_number-bb][4]});\n "
                line = line + " }\n "
                bb=bb-1
                if bb>=1:
                    while bb>0:
                        line = line + f" else if(huart->Instance=={uart_pin[uart_node_number-bb][0]})\n "
                        line = line + " {\n "
                        line = line + f" __HAL_RCC_{uart_pin[uart_node_number-bb][0]}_CLK_DISABLE();\n "
                        line = line + f" HAL_GPIO_DeInit(GPIO{uart_pin[uart_node_number-bb][1]}, GPIO_PIN_{uart_pin[uart_node_number-bb][2]});\n "
                        line = line + f" HAL_GPIO_DeInit(GPIO{uart_pin[uart_node_number-bb][3]}, GPIO_PIN_{uart_pin[uart_node_number-bb][4]});\n "
                        line = line + " }\n "
                        bb=bb-1
                line = line + " }\n "
            out_file.write(line)
    
    with open("main.c", "r") as in_file:
        buf = in_file.readlines()

    with open("main.c", "w") as out_file:
        for line in buf:
            if line == "/* Private variables */\n":
                while cc>0:
                    line = line + f" UART_HandleTypeDef {uart_pin[uart_node_number-cc][5]};\n "
                    cc=cc-1
            if line == "//Function prototype area\n":
                while dd>0:
                    line = line +f"static void MX_{uart_pin[uart_node_number-dd][0]}_UART_Init(void);\n"
                    dd=dd-1
            if line == "//Function calling area\n":
                while ee>0:
                    line = line +f"MX_{uart_pin[uart_node_number-ee][0]}_UART_Init();\n"
                    ee=ee-1 
            out_file.write(line)
    uartxxx=[[["", "","","",""], ["", "","","",""],["", "","","",""],["", "","","",""]],[["", "","","",""], ["", "","","",""],["", "","","",""],["", "","","",""]],[["", "","","",""], ["", "","","",""],["", "","","",""],["", "","","",""]],[["", "","","",""], ["", "","","",""],["", "","","",""],["", "","","",""]]]    
    uartyyy=[[["", "","","",""], ["", "","","",""],["", "","","",""],["", "","","",""]],[["", "","","",""], ["", "","","",""],["", "","","",""],["", "","","",""]],[["", "","","",""], ["", "","","",""],["", "","","",""],["", "","","",""]],[["", "","","",""], ["", "","","",""],["", "","","",""],["", "","","",""]]]    
    
    while ff>0:
        uart_direction[uart_node_number-ff]=int(input(f"0:{uart_pin[uart_node_number-ff][0]} only transmit , 1:{uart_pin[uart_node_number-ff][0]} only recieve,  2:{uart_pin[uart_node_number-ff][0]} transmit and recieve"))
        uart_baud[uart_node_number-ff]=int(input(f"{uart_pin[uart_node_number-ff][0]} baudrate="))

        if uart_direction[uart_node_number-ff]==0 or uart_direction[uart_node_number-ff]==2:
            uart_cont_trans[uart_node_number-ff]=int(input(f"0:{uart_pin[uart_node_number-ff][0]} transfer continous , 1:{uart_pin[uart_node_number-ff][0]} transfer one time"))
        else:
            uart_cont_trans[uart_node_number-ff]=0

        if uart_direction[uart_node_number-ff]==1 or uart_direction[uart_node_number-ff]==2:
            uart_cont_receive[uart_node_number-ff]=int(input(f"0:{uart_pin[uart_node_number-ff][0]} receive continous , 1:{uart_pin[uart_node_number-ff][0]} receive one time"))
        else:
            uart_cont_receive[uart_node_number-ff]=0

        if uart_direction[uart_node_number-ff]==0 or uart_direction[uart_node_number-ff]==2:
            print('Note:::You can enter transmited data as string and hexadecimal format.If data is string ,you must write like this "Hello". If data is hexadecimal format, you must write like this { 0x7e,0xfc, 0x7e }. And data can generate random variable like sensor value.If It include random value, you must type XXX where it should be.For example, "Temperature XXX" or { 0x7e, XXX, 0x7e } ')
            uart_transmit_data[uart_node_number-ff]=input(f"Transmitted data with {uart_pin[uart_node_number-ff][0]}= ")
            ada=int(input(f"How many randm variable exist {uart_pin[uart_node_number-uu][0]}? 0: has not random value"))
            count=ada
            if uart_cont_trans[uart_node_number-ff]==0 and ada>0:
                
                while count>0:
                        if uart_transmit_data[uart_node_number-ff].startswith("{"):
                            uartxxx[uart_node_number-ff][ada-count][4]= ada

                            uartxxx[uart_node_number-ff][ada-count][3]= "1"
                            uartxxx[uart_node_number-ff][ada-count][0]= input(f"What is the location of {(ada-count)+1}. random variable in array")
                            uartxxx[uart_node_number-ff][ada-count][1]= input(f"What is the upper limit of {(ada-count)+1}. random variable in array.Note:::Maximum range is between 0 and 255  because of uint8-t data type")
                            uartxxx[uart_node_number-ff][ada-count][2]= input(f"What is the lower limit of {(ada-count)+1}. random variable in array.Note:::Maximum range is between 0 and 255  because of uint8-t data type")
                        else:
                            uartxxx[uart_node_number-ff][ada-count][4]= ada
                            uartxxx[uart_node_number-ff][ada-count][3]= "0"
                            uartxxx[uart_node_number-ff][ada-count][0]= 0
                            uartxxx[uart_node_number-ff][ada-count][1]= input(f"What is the upper limit of {(ada-count)+1}. random variable in array.Note:::Maximum range is between 0 and 255  because of uint8-t data type")
                            uartxxx[uart_node_number-ff][ada-count][2]= input(f"What is the lower limit of {(ada-count)+1}. random variable in array.Note:::Maximum range is between 0 and 255  because of uint8-t data type")
                        count=count-1
            else :
                ada=0
                count=0
                uartxxx[uart_node_number-ff][ada-count][4]= 0

                uartxxx[uart_node_number-ff][ada-count][3]= ""
                uartxxx[uart_node_number-ff][ada-count][0]= ""
                uartxxx[uart_node_number-ff][ada-count][1]= ""
                uartxxx[uart_node_number-ff][ada-count][2]= ""

            

        else:
            uart_transmit_data[uart_node_number-ff]=""


        if uart_direction[uart_node_number-ff]==1 or uart_direction[uart_node_number-ff]==2:
            print('Note:::You can enter received data as string and hexadecimal format.If data is string ,you must write like this "Hello". If data is hexadecimal format, you must write like this { 0x7e,0xfc, 0x7e }. And data can include random variable like sensor value.If It include random value, you must type XXX where it should be.For example, "Temperature XXX" or { 0x7e, XXX, 0x7e } ')
            uart_receive_data[uart_node_number-ff]=input(f"Received data with {uart_pin[uart_node_number-ff][0]}= ")
            aka=int(input(f"How many random variable exist {uart_pin[uart_node_number-uu][0]}? 0: has not random value"))
            countyy=aka
            if uart_cont_receive[uart_node_number-ff]==0 and aka>0:
                
                while countyy>0:
                        if uart_receive_data[uart_node_number-ff].startswith("{"):
                            uartyyy[uart_node_number-ff][aka-countyy][4]= aka

                            uartyyy[uart_node_number-ff][aka-countyy][3]= "1"
                            uartyyy[uart_node_number-ff][aka-countyy][0]= input(f"What is the location of {(aka-countyy)+1}. random variable in array")
                            uartyyy[uart_node_number-ff][aka-countyy][1]= input(f"What is the upper limit of {(aka-countyy)+1}. random variable in array.Note:::Maximum range is between 0 and 255  because of uint8-t data type")
                            uartyyy[uart_node_number-ff][aka-countyy][2]= input(f"What is the lower limit of {(aka-countyy)+1}. random variable in array.Note:::Maximum range is between 0 and 255  because of uint8-t data type")
                        else:
                            uartyyy[uart_node_number-ff][aka-countyy][4]= aka
                            uartyyy[uart_node_number-ff][aka-countyy][3]= "0"
                            uartyyy[uart_node_number-ff][aka-countyy][0]= 0
                            uartyyy[uart_node_number-ff][aka-countyy][1]= input(f"What is the upper limit of {(aka-countyy)+1}. random variable in array.Note:::Maximum range is between 0 and 255  because of uint8-t data type")
                            uartyyy[uart_node_number-ff][aka-countyy][2]= input(f"What is the lower limit of {(aka-countyy)+1}. random variable in array.Note:::Maximum range is between 0 and 255  because of uint8-t data type")
                        countyy=countyy-1
            else :
                aka=0
                countyy=0
                uartyyy[uart_node_number-ff][aka-countyy][4]= 0

                uartyyy[uart_node_number-ff][aka-countyy][3]= ""
                uartyyy[uart_node_number-ff][aka-countyy][0]= ""
                uartyyy[uart_node_number-ff][aka-countyy][1]= ""
                uartyyy[uart_node_number-ff][aka-countyy][2]= ""

        else:
            uart_receive_data[uart_node_number-ff]=""
        ff=ff-1
        print(uartyyy)
        
    with open("main.c", "r") as in_file:
        buf = in_file.readlines()

    with open("main.c", "w") as out_file:
        for line in buf:
            if line == "/* Private user code */\n":
                ixix=1
                while gg>0:
                    if uart_direction[uart_node_number-gg]==0 or uart_direction[uart_node_number-gg]==2:
                                            
                        if uart_cont_trans[uart_node_number-gg]==0: 
                            man=uartxxx[uart_node_number-gg][0][4]
                            print(uartxxx)
                            print(man)
                            san=man
                            while san>0:
                                if uartxxx[uart_node_number-gg][0][3]=="1":
                                    uart_transmit_data[uart_node_number-gg]= uart_transmit_data[uart_node_number-gg].replace("XXX", "0x00", 1)
                                    
                                    san=san-1
                                elif uartxxx[uart_node_number-gg][0][3]=="0":
                                    uart_transmit_data[uart_node_number-gg]= uart_transmit_data[uart_node_number-gg].replace("XXX", "%d", 1)
                                    san=san-1
                            if uartxxx[uart_node_number-gg][0][3]=="0":
                                line = line + f' char sData{(uart_node_number-gg)*2}[{len(uart_transmit_data[uart_node_number-gg])+15}];\n '                            
                                line = line + f' uint8_t pData{(uart_node_number-gg)*2}[{len(uart_transmit_data[uart_node_number-gg])+15}];\n '
                            else:
                                line = line + f' uint8_t pData{(uart_node_number-gg)*2}[]={uart_transmit_data[uart_node_number-gg]};\n '
                        else:   
                            line = line + f' uint8_t pData{(uart_node_number-gg)*2}[]={uart_transmit_data[uart_node_number-gg]};\n '            
                        
                    if uart_direction[uart_node_number-gg]==1 or uart_direction[uart_node_number-gg]==2:
                        

                        if uartyyy[uart_node_number-gg][0][3]=="1":
                            uart_receive_data[uart_node_number-gg]= uart_receive_data[uart_node_number-gg].replace("XXX", "0x00", 1)
                            
                           
                        elif uartyyy[uart_node_number-gg][0][3]=="0":
                            uart_receive_data[uart_node_number-gg]= uart_receive_data[uart_node_number-gg].replace("XXX", "%d", 1)
                            
                        line = line + f' uint8_t pData{(uart_node_number-gg)*2+1}[{uart_receive_data[uart_node_number-gg].count(",")+1}]="{0}";\n ' 
                        line = line + f' uint8_t pData{(uart_node_number-gg)*2+1}comp[{uart_receive_data[uart_node_number-gg].count(",")+1}]={uart_receive_data[uart_node_number-gg]};\n ' 
                        line =line+f' int y{(uart_node_number-gg)*2+1};\n'
                        line =line+f' int sas{(uart_node_number-gg)*2+1}=0;\n'
                        line =line+f' int erroruart{ixix}=0;\n'
                       
                        
                    if uart_direction[uart_node_number-gg]==0 or uart_direction[uart_node_number-gg]==2:
                        if uart_cont_trans[uart_node_number-gg]==1:
                            line = line + f' HAL_UART_Transmit(&{uart_pin[uart_node_number-gg][5]}, pData{(uart_node_number-gg)*2}, sizeof(pData{(uart_node_number-gg)*2}), 1000);\n '              
                            line = line + f' HAL_Delay(250);\n'     
                            line = line + f'//End of {uart_pin[uart_node_number-gg][0]}Transmit\n '  
                    if uart_direction[uart_node_number-gg]==1 or uart_direction[uart_node_number-gg]==2:
                        if uart_cont_receive[uart_node_number-gg]==1:
                            line = line + f'//Begin of {uart_pin[uart_node_number-gg][0]}Receive\n '  
                            line = line + f' HAL_UART_Receive(&{uart_pin[uart_node_number-gg][5]}, pData{(uart_node_number-gg)*2+1}, sizeof(pData{(uart_node_number-gg)*2}), 1000);\n '              
                            line = line + f'HAL_Delay(250);\n'          
                            line = line + f'//End of {uart_pin[uart_node_number-gg][0]}Receive\n '            
                    gg=gg-1
            if line == "//Inside of the infinite loop in main function\n":
                while hh>0:
                    if uart_direction[uart_node_number-hh]==0 or uart_direction[uart_node_number-hh]==2:
                        if uart_cont_trans[uart_node_number-hh]==0:
                            dan=uartxxx[uart_node_number-hh][0][4]
                            ban=dan
                            while ban>0:
                                if uartxxx[uart_node_number-hh][0][3]=="1":
                                    
                                    line = line + f' int x{uart_node_number-hh}{dan-ban}=rand()%{int(uartxxx[uart_node_number-hh][dan-ban][1])-int(uartxxx[uart_node_number-hh][dan-ban][2])+1}+{int(uartxxx[uart_node_number-hh][dan-ban][2])};\n ' 
                                    line = line + f' pData{(uart_node_number-hh)*2}[{uartxxx[uart_node_number-hh][dan-ban][0]}] = (uint8_t) x{uart_node_number-hh}{dan-ban} ;\n '
                                    ban=ban-1
                                elif uartxxx[uart_node_number-hh][0][3]=="0":
                                    line = line + f' int x{uart_node_number-hh}{dan-ban}=rand()%{int(uartxxx[uart_node_number-hh][dan-ban][1])-int(uartxxx[uart_node_number-hh][dan-ban][2])+1}+{int(uartxxx[uart_node_number-hh][dan-ban][2])};\n ' 
                                    ban=ban-1
                                
                            if uartxxx[uart_node_number-hh][0][3]=="0":        
                                if dan==1:
                                    line = line + f' 	sprintf(sData{(uart_node_number-hh)*2}, {uart_transmit_data[uart_node_number-hh]},x{uart_node_number-hh}{dan-ban});\n '
                                elif dan==2:
                                    line = line + f' 	sprintf(sData{(uart_node_number-hh)*2}, {uart_transmit_data[uart_node_number-hh]},x{uart_node_number-hh}{0},x{uart_node_number-hh}{1});\n '
                                elif dan==3:
                                    line = line + f' 	sprintf(sData{(uart_node_number-hh)*2}, {uart_transmit_data[uart_node_number-hh]},x{uart_node_number-hh}{0},x{uart_node_number-hh}{1},x{uart_node_number-hh}{2});\n '
                                elif dan==4:
                                    line = line + f' 	sprintf(sData{(uart_node_number-hh)*2}, {uart_transmit_data[uart_node_number-hh]},x{uart_node_number-hh}{0},x{uart_node_number-hh}{1},x{uart_node_number-hh}{2},x{uart_node_number-hh}{3});\n '
                                                
                                line = line + f' for(int k=0; k==strlen(sData{(uart_node_number-hh)*2});k++)\n '    
                                line = line + ' {\n '       
                                line = line + f' pData{(uart_node_number-hh)*2}[k]= (uint8_t)sData{(uart_node_number-hh)*2}[k];\n '  
                                line = line + ' }\n '    
                            line = line + f'//Begin of transmit {uart_pin[uart_node_number-hh][0]}\n '
                            line = line + f' HAL_UART_Transmit(&{uart_pin[uart_node_number-hh][5]}, pData{(uart_node_number-hh)*2}, sizeof(pData{(uart_node_number-hh)*2}), 1000);\n '              
                            line = line + f'HAL_Delay(250);\n' 
                            line = line + f'//End of {uart_pin[uart_node_number-hh][0]}Transmit\n'  
                    if uart_direction[uart_node_number-hh]==1 or uart_direction[uart_node_number-hh]==2:
                        if uart_cont_receive[uart_node_number-hh]==0:
                            line = line + f'//Begin of {uart_pin[uart_node_number-hh][0]}Receive\n'  
                            line = line + f' HAL_UART_Receive(&{uart_pin[uart_node_number-hh][5]}, pData{(uart_node_number-hh)*2+1}, sizeof(pData{(uart_node_number-hh)*2+1}), 1000);\n '              
                            line = line + f' HAL_Delay(250);\n ' 
                            
                            lux=uartyyy[uart_node_number-hh][0][4]
                            lun=lux
                            line = line + f' for (y{(uart_node_number-hh)*2+1}=0; y{(uart_node_number-hh)*2+1}<sizeof(pData{(uart_node_number-hh)*2+1}); y{(uart_node_number-hh)*2+1}++)\n ' 
                            line = line + '{\n ' 
                            while lun>0:
                                if lux-lun==0:    
                                    line = line + f'if (y{(uart_node_number-hh)*2+1}=={uartyyy[uart_node_number-hh][lux-lun][0]})\n '
                                    line = line + '{\n ' 
                                    line = line + f'if (pData{(uart_node_number-hh)*2+1}[y{(uart_node_number-hh)*2+1}]>={hex(int(uartyyy[uart_node_number-hh][lux-lun][2]))} && pData{(uart_node_number-hh)*2+1}[y{(uart_node_number-hh)*2+1}]<={hex(int(uartyyy[uart_node_number-hh][lux-lun][1]))})\n ' 
                                    line = line + "{\n"
                                    line = line + f"sas{(uart_node_number-hh)*2+1}++;\n"
                                    line = line + "} }\n"
                            
                                elif lun>0:
                                    line = line + f'else if (y{(uart_node_number-hh)*2+1}=={uartyyy[uart_node_number-hh][lux-lun][0]})\n '
                                    line = line + '{\n ' 
                                    line = line + f'if (pData{(uart_node_number-hh)*2+1}[y{(uart_node_number-hh)*2+1}]>={hex(int(uartyyy[uart_node_number-hh][lux-lun][2]))} && pData{(uart_node_number-hh)*2+1}[y{(uart_node_number-hh)*2+1}]<={hex(int(uartyyy[uart_node_number-hh][lux-lun][1]))})\n ' 
                                    line = line + "{\n"
                                    line = line + f"sas{(uart_node_number-hh)*2+1}++;\n"
                                    line = line + "} }\n"
                                lun =lun-1        
                            if uart_receive_data[uart_node_number-hh].count(",")+1!=0 and lux>0:
                                line = line + f'else \n '
                                line = line + '{\n ' 
                                line = line + f'if (pData{(uart_node_number-hh)*2+1}[y{(uart_node_number-hh)*2+1}]==pData{(uart_node_number-hh)*2+1}comp[y{(uart_node_number-hh)*2+1}] )\n ' 
                                line = line + "{\n"
                                line = line + f"sas{(uart_node_number-hh)*2+1}++;\n"
                                line = line + "} }\n"
                            else :
                                line = line + f'if (pData{(uart_node_number-hh)*2+1}[y{(uart_node_number-hh)*2+1}]==pData{(uart_node_number-hh)*2+1}comp[y{(uart_node_number-hh)*2+1}] )\n ' 
                                line = line + "{\n"
                                line = line + f"sas{(uart_node_number-hh)*2+1}++;\n"
                                line = line + "} }\n"
                    
                            if lux>0:        
                                line = line + "}\n"
                            line=line +f" if  (sas{(uart_node_number-hh)*2+1} != sizeof(pData{(uart_node_number-hh)*2+1}))\n"
                            line=line +"{\n"
                            line=line +f" erroruart{ixix}++;\n"
                            line=line +"}\n"
                            line=line +"else\n"
                            line=line +"{\n"
                            line=line +f" erroruart{ixix}=0;\n"
                            line=line +"}\n"
                            line=line +f"sas{(uart_node_number-hh)*2+1}=0 ;\n"
                            line=line +f"y{(uart_node_number-hh)*2+1}=0 ;\n"                   
                            line = line + f'//End of {uart_pin[uart_node_number-hh][0]}Receive\n'    
                            ixix=ixix+1     
                    hh=hh-1


            if line == "//Function area\n":
                while uu>0:
                    line = line + f'static void MX_{uart_pin[uart_node_number-uu][0]}_UART_Init(void)\n ' 
                    line = line + '{\n ' 
                    line = line + f'  {uart_pin[uart_node_number-uu][5]}.Instance = {uart_pin[uart_node_number-uu][0]};\n ' 
                    line = line + f'  {uart_pin[uart_node_number-uu][5]}.Init.BaudRate = {uart_baud[uart_node_number-uu]};\n ' 
                    line = line + f'  {uart_pin[uart_node_number-uu][5]}.Init.WordLength = UART_WORDLENGTH_8B;\n ' 
                    line = line + f'  {uart_pin[uart_node_number-uu][5]}.Init.StopBits = UART_STOPBITS_1;\n ' 
                    line = line + f'  {uart_pin[uart_node_number-uu][5]}.Init.Parity = UART_PARITY_NONE;\n ' 
                    line = line + f'    {uart_pin[uart_node_number-uu][5]}.Init.Mode = UART_MODE_TX_RX;\n ' 
                    line = line + f'    {uart_pin[uart_node_number-uu][5]}.Init.HwFlowCtl = UART_HWCONTROL_NONE;\n ' 
                    line = line + f'    {uart_pin[uart_node_number-uu][5]}.Init.OverSampling = UART_OVERSAMPLING_16;\n ' 
                    line = line + f'    if (HAL_UART_Init(&{uart_pin[uart_node_number-uu][5]}) != HAL_OK)\n ' 
                    line = line + '      {\n ' 
                    line = line + f'    Error_Handler();\n ' 
                    line = line + '   }}\n' 
                    uu=uu-1                  
            out_file.write(line)
                


def PWM_checker(PWM_output):
    
    zz=PWM_output
    yy=PWM_output
    gg=PWM_output
    aa=PWM_output
    bb=PWM_output
    dd=PWM_output
    ee=PWM_output
    hh=PWM_output
    mol=PWM_output
    sa=PWM_output
    da=PWM_output
    xx=PWM_output
    with open("stm32f4xx_hal_conf.h", "r") as in_file:
        buf = in_file.readlines()

    with open("stm32f4xx_hal_conf.h", "w") as out_file:
        for line in buf:
            if line == "/* #define HAL_TIM_MODULE_ENABLED   */\n":
                line = "#define HAL_TIM_MODULE_ENABLED\n"
            out_file.write(line)

    with open("stm32f4xx_it.h", "r") as in_file:
        buf = in_file.readlines()

    with open("stm32f4xx_it.h", "w") as out_file:
        for line in buf:
            if line == "void OTG_FS_IRQHandler(void);\n":
                while gg>=1:
                    line = line + f"void {c[PWM_output-gg][0]}_IRQHandler(void);\n"
                    gg-=1                   
            out_file.write(line)

    with open("stm32f4xx_hal_msp.c", "r") as in_file:
        buf = in_file.readlines()

    with open("stm32f4xx_hal_msp.c", "w") as out_file:
        for line in buf:
            if line ==  "/* USER CODE BEGIN 1 */\n":
                line = line + "void HAL_TIM_Base_MspInit(TIM_HandleTypeDef* htim_base)\n"
                line = line + "{\n"
                line = line + "  GPIO_InitTypeDef GPIO_InitStruct = {0};\n"
                line = line + f"  if(htim_base->Instance=={c[PWM_output-zz][0]})\n"
                line = line + "  {\n"
                line = line + f"    __HAL_RCC_{c[PWM_output-zz][0]}_CLK_ENABLE();\n"
                line = line + f"    __HAL_RCC_GPIO{c[PWM_output-zz][2]}_CLK_ENABLE();\n"
                line = line + f"    GPIO_InitStruct.Pin = GPIO_PIN_{c[PWM_output-zz][3]};\n"
                line = line + "    GPIO_InitStruct.Mode = GPIO_MODE_AF_PP;\n"
                line = line + "    GPIO_InitStruct.Pull = GPIO_NOPULL;\n"
                line = line + "    GPIO_InitStruct.Speed = GPIO_SPEED_FREQ_LOW;\n"
                line = line + f"    GPIO_InitStruct.Alternate = GPIO_AF1_{c[PWM_output-zz][0]};\n"
                line =line + f"    HAL_GPIO_Init(GPIO{c[PWM_output-zz][2]}, &GPIO_InitStruct);\n"
                line = line +f"    HAL_NVIC_SetPriority({c[PWM_output-zz][0]}_IRQn, 0, 0);\n"
                line = line +f"    HAL_NVIC_EnableIRQ({c[PWM_output-zz][0]}_IRQn);\n"
                line = line +"      }\n"
                zz-=1
                if zz>=1:
                    while zz>0:
                        line =line + f" else if(htim_base->Instance=={c[PWM_output-zz][0]})\n"
                        line =line + " {\n"
                        line =line + f"    __HAL_RCC_{c[PWM_output-zz][0]}_CLK_ENABLE();\n"
                        line = line +f"    __HAL_RCC_GPIO{c[PWM_output-zz][2]}_CLK_ENABLE();\n"
                        line =line +f"    GPIO_InitStruct.Pin = GPIO_PIN_{c[PWM_output-zz][3]};\n"
                        line =line + "    GPIO_InitStruct.Mode = GPIO_MODE_AF_PP;\n"
                        line = line +"    GPIO_InitStruct.Pull = GPIO_NOPULL;\n"
                        line = line +"    GPIO_InitStruct.Speed = GPIO_SPEED_FREQ_LOW;\n"
                        line = line +f"    GPIO_InitStruct.Alternate = GPIO_AF2_{c[PWM_output-zz][0]};\n"
                        line = line +f"    HAL_GPIO_Init(GPIO{c[PWM_output-zz][2]}, &GPIO_InitStruct);\n"
                        line = line +f"    HAL_NVIC_SetPriority({c[PWM_output-zz][0]}_IRQn, 0, 0);\n"
                        line = line +f"    HAL_NVIC_EnableIRQ({c[PWM_output-zz][0]}_IRQn);\n"
                        line = line +"      }\n"
                        zz-=1
                line = line +"      }\n"
                
                line = line +" void HAL_TIM_Base_MspDeInit(TIM_HandleTypeDef* htim_base)\n"
                line = line +"{\n"
                line = line +f"     if(htim_base->Instance=={c[PWM_output-yy][0]})\n"
                line = line +"    {\n"
                line = line +f"  __HAL_RCC_{c[PWM_output-yy][0]}_CLK_DISABLE();\n"
                line = line +f"  /**{c[PWM_output-yy][0]} GPIO Configuration\n"
                line = line +"      */\n"
                line = line +f"      HAL_GPIO_DeInit(GPIO{c[PWM_output-yy][2]}, GPIO_PIN_{c[PWM_output-yy][3]});\n"
                line = line +f"    HAL_NVIC_DisableIRQ({c[PWM_output-yy][0]}_IRQn);\n"
                line = line +"         }\n"
                yy-=1
                if yy>=1:
                    while yy>0:
                        line =line + f"  else if(htim_base->Instance=={c[PWM_output-yy][0]})\n"
                        line =line + "  {\n"
                        line = line +f"       __HAL_RCC_{c[PWM_output-yy][0]}_CLK_DISABLE();\n"
                        line = line +f"           /**{c[PWM_output-yy][0]} GPIO Configuration\n"
                        line = line +f"            P{c[PWM_output-yy][2]}{c[PWM_output-yy][3]}     ------> {c[PWM_output-yy][0]}_CH1\n"
                        line = line +"          */\n"
                    
                        
                        line = line +f"        HAL_GPIO_DeInit(GPIO{c[PWM_output-yy][2]}, GPIO_PIN_{c[PWM_output-yy][3]});\n"
                        line = line +f"             HAL_NVIC_DisableIRQ({c[PWM_output-yy][0]}_IRQn);\n"
                        line = line +"           }\n"
                    
                        yy-=1
                line = line +"     }\n"        
                    
            out_file.write(line)

    with open("stm32f4xx_it.c", "r") as in_file:
        buf = in_file.readlines()

    with open("stm32f4xx_it.c", "w") as out_file:
        for line in buf:
            if line == "/* USER CODE BEGIN 1 */\n":
                while aa>0:
                        line =line + f" void {c[PWM_output-aa][0]}_IRQHandler(void)\n"
                        line =line + "  {\n"
                        line = line +f"         HAL_TIM_IRQHandler(&htim{c[PWM_output-aa][1]});\n"
                        line = line +"        }\n"
                        aa-=1
            if line == "/* External variables --------------------------------------------------------*/\n":
                while bb>0:
                    line =line + f" extern TIM_HandleTypeDef htim{c[PWM_output-bb][1]};\n"
                    bb-=1

            out_file.write(line)
    with open("main.c", "r") as in_file:
        buf = in_file.readlines()

    with open("main.c", "w") as out_file:
        for line in buf:
            if line == "/* Private variables */\n":
                while dd>0:
                    line = line + f"TIM_HandleTypeDef htim{c[PWM_output-dd][1]};\n"
                    dd-=1
            if line == "//Function prototype area\n":
                line = line + "void Delay_ms(volatile int time_ms);\n"
                while ee>0:
                    line = line + f"static void MX_{c[PWM_output-ee][0]}_Init(void);\n"     
                    ee-=1  
            if line == "/* Private user code */\n":
                while hh>0:
                    line =line +f"__IO uint32_t ICValue{PWM_output-hh+1}=0;\n" 
                    line =line +f"__IO uint32_t Frequency{PWM_output-hh+1}=0;\n" 
                    line =line +f"__IO uint32_t Duty{PWM_output-hh+1}=0;\n" 
                    hh-=1  
                line =line +f"__IO uint32_t i={PWM_output};\n"
                line =line +"void HAL_TIM_IC_CaptureCallback(TIM_HandleTypeDef *htim)\n"
                line =line +"   {\n"
                line =line +f"      if(htim->Channel==HAL_TIM_ACTIVE_CHANNEL_1)\n"
                line =line +"      {\n"
                line =line +f"          if(i=={c[PWM_output-mol][1]})\n"
                line= line +"               {\n"
                line =line +f"                   ICValue{PWM_output-mol+1}=HAL_TIM_ReadCapturedValue(htim,TIM_CHANNEL_1);\n"
                line= line +f"                      if(ICValue{PWM_output-mol+1}!=0)\n"
                line= line +"                           {\n"
                line =line +f"                              Duty{PWM_output-mol+1}=(HAL_TIM_ReadCapturedValue(htim,TIM_CHANNEL_2)*100)/ICValue{PWM_output-mol+1}+1;\n"
                line =line +f"                              Frequency{PWM_output-mol+1}=((HAL_RCC_GetHCLKFreq())/2/ICValue{PWM_output-mol+1})/10;\n"
                line =line +"                              }\n"                
                line =line +"                 }\n"
                mol-=1
                while mol>0:
                    line =line +f"      else if(i=={c[PWM_output-mol][1]})\n"
                    line =line +"           {\n"
                    line =line +f"              ICValue{PWM_output-mol+1}=HAL_TIM_ReadCapturedValue(htim,TIM_CHANNEL_1);\n"
                    line =line +f"                  if(ICValue{PWM_output-mol+1}!=0)\n"
                    line =line +"                       {\n"
                    
                    line =line +f"                          Duty{PWM_output-mol+1}=((HAL_TIM_ReadCapturedValue(htim,TIM_CHANNEL_2)*100)/ICValue{PWM_output-mol+1})+1;\n"
                    line =line +f"                          Frequency{PWM_output-mol+1}=((HAL_RCC_GetHCLKFreq())/2/ICValue{PWM_output-mol+1})/10;\n"
                    line =line +"                      	}\n"
                    line =line +"             }\n"
                    mol-=1
                line =line+"}\n"
                line =line+"        }\n"
            if line == "//Function calling area\n":
                while sa>0:
                    line =line +f"  MX_{c[PWM_output-sa][0]}_Init();\n"
                    sa-=1
            if line == "//Inside of the infinite loop in main function\n":
                line =line +f"ICValue{PWM_output-da+1}=0;\n"
                line =line +f"  Duty{PWM_output-da+1}=0;\n"
                line =line +f"  Frequency{PWM_output-da+1}=0;\n"
                
                line =line +f"//Begin of PWM{PWM_output-da+1}\n"
                line =line +f" HAL_TIM_IC_Start_IT(&htim{c[PWM_output-da][1]},TIM_CHANNEL_1);\n"
                line =line +f" HAL_TIM_IC_Start_IT(&htim{c[PWM_output-da][1]},TIM_CHANNEL_2);\n"
                line =line +"Delay_ms(200);\n"
                line =line +f" HAL_TIM_IC_Stop_IT(&htim{c[PWM_output-da][1]},TIM_CHANNEL_1);\n"
                line =line +f" HAL_TIM_IC_Stop_IT(&htim{c[PWM_output-da][1]},TIM_CHANNEL_2);\n"                
                da-=1    
                if da>0:
                    line =line +f" i={c[PWM_output-da+1][1]};\n"
                    line =line +"Delay_ms(212);\n"    
                    line =line +f"//End of PWM{PWM_output-da}\n"   
                else:
                    line =line +f" i=2;\n"
                    line =line +"Delay_ms(212);\n"    
                    line =line +f"//End of PWM{PWM_output-da}\n"                                           
                while da>0:
                    line =line +f"//Begin of PWM{PWM_output-da+1}\n"
                    line =line +f"ICValue{PWM_output-da+1}=0;\n"
                    line =line +f"  Duty{PWM_output-da+1}=0;\n"
                    line =line +f"  Frequency{PWM_output-da+1}=0;\n"
                    line =line +f" HAL_TIM_IC_Start_IT(&htim{c[PWM_output-da][1]},TIM_CHANNEL_1);\n"
                    line =line +f" HAL_TIM_IC_Start_IT(&htim{c[PWM_output-da][1]},TIM_CHANNEL_2);\n"
                    line =line +"Delay_ms(200);\n"
                    line =line +f" HAL_TIM_IC_Stop_IT(&htim{c[PWM_output-da][1]},TIM_CHANNEL_1);\n"
                    line =line +f" HAL_TIM_IC_Stop_IT(&htim{c[PWM_output-da][1]},TIM_CHANNEL_2);\n"  
                    if da>1:
                        line =line +f" i={c[PWM_output-da+1][1]};\n"
                    elif da==1:
                        line =line +f" i={c[0][1]};\n"

                    line =line +"Delay_ms(212);\n" 
                    line =line +f"//End of PWM{PWM_output-da+1}\n" 
                    da-=1

            
            if line == "//Function area\n":
                line =line+"void Delay_ms(volatile int time_ms){\n"                
                line =line+"int j;\n"
                line =line+" for(j = 0; j < time_ms*4000; j++)\n"
                line =line+" {}  \n"
                line =line+" }  \n"
            if line == "//Timer config  area\n":
                while xx>0:
                    line =line+f"static void MX_{c[PWM_output-xx][0]}_Init(void)\n"                
                    line =line+"{\n"
                    line =line+" TIM_ClockConfigTypeDef sClockSourceConfig = {0};\n"
                    line =line+"TIM_SlaveConfigTypeDef sSlaveConfig = {0}; \n"
                    line =line+"TIM_IC_InitTypeDef sConfigIC = {0}; \n"    
                    line =line+"   TIM_MasterConfigTypeDef sMasterConfig = {0};\n"
                    line =line+f"htim{c[PWM_output-xx][1]}.Instance = TIM{c[PWM_output-xx][1]}; \n"
                    line =line+f"htim{c[PWM_output-xx][1]}.Init.Prescaler = 16; \n" 
                    line =line+f" htim{c[PWM_output-xx][1]}.Init.CounterMode = TIM_COUNTERMODE_UP;\n"
                    line =line+f"  htim{c[PWM_output-xx][1]}.Init.Period = 4294967295; \n"
                    line =line+f"htim{c[PWM_output-xx][1]}.Init.ClockDivision = TIM_CLOCKDIVISION_DIV1; \n" 
                    line =line+f"   htim{c[PWM_output-xx][1]}.Init.AutoReloadPreload = TIM_AUTORELOAD_PRELOAD_DISABLE;\n"
                    line =line+f"  if (HAL_TIM_Base_Init(&htim{c[PWM_output-xx][1]}) != HAL_OK) \n"
                    line =line+"  { \n"    
                    line =line+"      Error_Handler();\n"
                    line =line+"} \n"
                    line =line+"  sClockSourceConfig.ClockSource = TIM_CLOCKSOURCE_INTERNAL; \n" 
                    line =line+f"   if (HAL_TIM_ConfigClockSource(&htim{c[PWM_output-xx][1]}, &sClockSourceConfig) != HAL_OK)\n"
                    line =line+"    { \n"
                    line =line+"    Error_Handler(); \n" 
                    line =line+"} \n"
                    line =line+f"    if (HAL_TIM_IC_Init(&htim{c[PWM_output-xx][1]}) != HAL_OK) \n"
                    line =line+"  { \n"    
                    line =line+"      Error_Handler();\n"
                    line =line+"} \n"
                    line =line+"   sSlaveConfig.SlaveMode = TIM_SLAVEMODE_RESET;\n" 
                    line =line+"     sSlaveConfig.InputTrigger = TIM_TS_TI1FP1;\n"
                    line =line+"   sSlaveConfig.TriggerPolarity = TIM_INPUTCHANNELPOLARITY_RISING;\n"
                    line =line+"    sSlaveConfig.TriggerPrescaler = TIM_ICPSC_DIV1; \n" 
                    line =line+" sSlaveConfig.TriggerFilter = 0; \n"
                    line =line+f"   if (HAL_TIM_SlaveConfigSynchro(&htim{c[PWM_output-xx][1]}, &sSlaveConfig) != HAL_OK)\n" 
                    line =line+"       {\n"
                    line =line+"    Error_Handler();\n"
                    line =line+"     } \n"          
                    line =line+"     sConfigIC.ICPolarity = TIM_INPUTCHANNELPOLARITY_RISING;\n" 
                    line =line+"       sConfigIC.ICSelection = TIM_ICSELECTION_DIRECTTI;\n"
                    line =line+"   sConfigIC.ICPrescaler = TIM_ICPSC_DIV1;\n"
                    line =line+"     sConfigIC.ICFilter = 0; \n" 
                    line =line+f"  if (HAL_TIM_IC_ConfigChannel(&htim{c[PWM_output-xx][1]}, &sConfigIC, TIM_CHANNEL_1) != HAL_OK) \n"
                    line =line+"       {\n"
                    line =line+"    Error_Handler();\n"
                    line =line+"     } \n" 
                    line =line+"      sConfigIC.ICPolarity = TIM_INPUTCHANNELPOLARITY_FALLING;\n" 
                    line =line+"         sConfigIC.ICSelection = TIM_ICSELECTION_INDIRECTTI;\n"
                    line =line+f"    if (HAL_TIM_IC_ConfigChannel(&htim{c[PWM_output-xx][1]}, &sConfigIC, TIM_CHANNEL_2) != HAL_OK)\n"
                    line =line+"       {\n"
                    line =line+"    Error_Handler();\n"
                    line =line+"     } \n" 
                    line =line+"        sMasterConfig.MasterOutputTrigger = TIM_TRGO_RESET;\n" 
                    line =line+"           sMasterConfig.MasterSlaveMode = TIM_MASTERSLAVEMODE_DISABLE;\n"
                    line =line+f"      if (HAL_TIMEx_MasterConfigSynchronization(&htim{c[PWM_output-xx][1]}, &sMasterConfig) != HAL_OK)\n"
                    line =line+"       {\n"
                    line =line+"    Error_Handler();\n"
                    line =line+"     } \n" 
                    line =line+"     } \n" 
                    xx-=1

            out_file.write(line)






                
                



                        
def match():

    astab=number_of_PWM
    klkl=number_of_UART
    slsls=hasya
    qlqlql=masya
    
    if number_of_ADC==1:
        asasa=len(dac1up_range)
        while asasa>0:
            sumreason.append(f"DAC1-{dac1up_range[len(dac1low_range)-asasa]},{dac1low_range[len(dac1low_range)-asasa]}")
            asasa=asasa-1
    if number_of_ADC==2:
        sasas=len(dac1low_range)
        sastas=len(dac2low_range)
        while sasas>0:
            sumreason.append(f"DAC1-{dac1up_range[len(dac1low_range)-sasas]},{dac1low_range[len(dac1low_range)-sasas]}")
            sasas=sasas-1
        while sastas>0:
            sumreason.append(f"DAC2-{dac2up_range[len(dac2low_range)-sastas]},{dac2low_range[len(dac2low_range)-sastas]}")
            sastas=sastas-1
    while astab>0:
        duty.append(input(f"Duty cyle of PWM{number_of_PWM-astab+1}"))
        frequency.append(input(f"Frequency of PWM{number_of_PWM-astab+1}"))
        sumresult.append(f"PWM{number_of_PWM-astab+1}-{frequency[number_of_PWM-astab]}")
        astab=astab-1
    while klkl>0:
        if uart_direction[number_of_UART-klkl]==0:
            sumreason.append(f"{uart_pin[number_of_UART-klkl][0]}Transmit")
        elif uart_direction[number_of_UART-klkl]==1:
            sumresult.append(f"{uart_pin[number_of_UART-klkl][0]}Receive")
        elif uart_direction[number_of_UART-klkl]==2:
            sumreason.append(f"{uart_pin[number_of_UART-klkl][0]}Transmit")
            sumresult.append(f"{uart_pin[number_of_UART-klkl][0]}Receive")
        klkl=klkl-1
    while slsls>0:
        sumresult.append(f"GPIO_IN{hasya-slsls+1}")
        slsls=slsls-1
    while qlqlql>0:
        sumreason.append(f"GPIO_OUT{masya-qlqlql+1}")
        qlqlql=qlqlql-1
    print(f"Resaon node:{sumreason}")
    print(f"Result node:{sumresult}")
    input2=input("Result node?")
    input1=input("Reason node?")
    
    while input2!="" and input1!="":
        
        pixi=1
        if input2.startswith("GPIO"):
            errorsum.append(f"errorIn{input2[len(input2)-1]}")
            writing = False
            denepp=[]
            with open("main.c", "r") as in_file:
                buf = in_file.readlines()
            with open("main.c", "w") as out_file:
                for line in buf:
                    if line == f'//Begin of {input2}\n':
                        writing = True
                    elif line== f'//End of {input2}\n':    
                        writing = False
                    if writing:
                        denepp.append(line)
                        line=""
                    out_file.write(line)
        elif input2.startswith("UART"):
            errorsum.append(f"erroruart{pixi}")
            pixi=pixi+1
            writing = False
            denepp=[]
            with open("main.c", "r") as in_file:
                buf = in_file.readlines()
            with open("main.c", "w") as out_file:
                for line in buf:
                    if line == f'//Begin of {input2}\n':
                        writing = True
                    elif line== f'//End of {input2}\n':    
                        writing = False
                    if writing:
                        denepp.append(line)
                        line=""
                    out_file.write(line)


                
                    



                    

        elif input2.startswith("PWM"):
            errorsum.append(f"errorduty{input2[0:4]}")
            errorsum.append(f"errorfreq{input2[0:4]}")
            writing = False
            denepp=[]
            with open("main.c", "r") as in_file:
                buf = in_file.readlines()
            with open("main.c", "w") as out_file:
                for line in buf:
                    if line == "/* Private variables */\n":
                        
                        line= line +f"int errorduty{input2[0:4]}=0;\n"
                        line= line +f"int errorfreq{input2[0:4]}=0;\n"
                    if line == f'//Begin of {input2[0:4]}\n':
                        writing = True
                    elif line== f'//End of {input2[0:4]}\n':    
                        writing = False
                    if writing:
                        denepp.append(line)
                        line=""
                    
                    out_file.write(line)

            denepp.append(f"if ( Duty{input2[3]}== {duty[int(input2[3])-1]})")
            denepp.append("{")
            denepp.append(f"errorduty{input2[0:4]}++;")
            denepp.append("}")
            denepp.append("else")
            denepp.append("{")
            denepp.append(f"errorduty{input2[0:4]}=0;")
            denepp.append("}")
            
            denepp.append(f"if (Frequency{input2[3]} == {frequency[int(input2[3])-1]})")
            denepp.append("{")
            denepp.append(f"errorfreq{input2[0:4]}++;")
            denepp.append("}")
            denepp.append("else")
            denepp.append("{")
            denepp.append(f"errorfreq{input2[0:4]}=0;")
            denepp.append("}")

            if input2.startswith("PWM") :
                if input1.startswith("DAC"):
                    with open("main.c", "r") as in_file:
                        buf = in_file.readlines()
                    with open("main.c", "w") as out_file:
                        for line in buf:
                      
                            if line == f" {input1[0:4]}_voltage=0;\n":
                                line= f"{input1[0:4]}_voltage++;\n"
                                line=line + f"{input1[0:4]}_voltage={input1[0:4]}_voltage%4095;\n\n"
                            if line.startswith(f"if ( Duty{input2[3]}== {duty[int(input2[3])-1]})"):
                                line="if ( Duty{input2[3]}==({input1[0:4]}_voltage * (100/4095)) )"
                             
                            out_file.write(line)





            

        



        if input1.startswith("GPIO"):
            with open("main.c", "r") as in_file:
                buf = in_file.readlines()
            with open("main.c", "w") as out_file:
                for line in buf:
                    if line == f'//End of {input1}\n':
                        for x in denepp:
                            line=line+f"{x}\n"
                    out_file.write(line)
        elif input1.startswith("DAC"):
            with open("main.c", "r") as in_file:
                buf = in_file.readlines()
            with open("main.c", "w") as out_file:
                for line in buf:
                    if line == f'//End of {input1}\n':
                        for x in denepp:
                            line=line+f"{x}\n"
                    out_file.write(line)
        elif input1.startswith("UART"):
            with open("main.c", "r") as in_file:
                buf = in_file.readlines()
            with open("main.c", "w") as out_file:
                for line in buf:
                    if line == f'//End of {input1}\n':
                        for x in denepp:
                            line=line+f"{x}\n"
                    out_file.write(line)
        if input2.startswith("UART"):
            if input1.startswith("UART"):
                with open("main.c", "r") as in_file:
                    buf = in_file.readlines()
                with open("main.c", "w") as out_file:
                    for line in buf:
                        if line.startswith(f'  HAL_UART_Transmit(&huart{input1[4]}'):
                            banb=line[29:35]
                            print(banb)  
                        out_file.write(line)

            if input1.startswith("UART"):
                with open("main.c", "r") as in_file:
                    buf = in_file.readlines()
                with open("main.c", "w") as out_file:
                    for line in buf:
                        if line.startswith(f' HAL_UART_Receive(&huart{input2[4]}'):
                            danb=line[27:33]
                            print(danb) 
                        out_file.write(line)


            if input1.startswith("UART"):
                with open("main.c", "r") as in_file:
                    buf = in_file.readlines()
                with open("main.c", "w") as out_file:
                    for line in buf:
                        
                        if line == f'//Begin of {input2}\n':
                            
                            line=line+f"for(int ix=0;ix<sizeof({danb}comp) ;ix++)\n"
                            line=line+"{"
                            line=line+f"{danb}comp[ix]={banb}[ix];\n"
                            line=line+"}\n"
                            

                        out_file.write(line)
            
        

        

            

    
        input2=input("Result node?")
        input1=input("Reason node?")
        




    











               
                
        
    

src= r'D:\empty-driver\stm32f4xx_hal_conf.h'
dst = r'C:\Users\enver\Desktop\bitirme-yedek\16.10 yedek\stm32f4xx_hal_conf.h'
shutil.copyfile(src, dst)
src= r'D:\empty-driver\stm32f4xx_it.h'
dst = r'C:\Users\enver\Desktop\bitirme-yedek\16.10 yedek\stm32f4xx_it.h'
shutil.copyfile(src, dst)
src= r'D:\empty-driver\stm32f4xx_hal_msp.c'
dst = r'C:\Users\enver\Desktop\bitirme-yedek\16.10 yedek\stm32f4xx_hal_msp.c'
shutil.copyfile(src, dst)
src= r'D:\empty-driver\stm32f4xx_it.c' 
dst = r'C:\Users\enver\Desktop\bitirme-yedek\16.10 yedek\stm32f4xx_it.c'
shutil.copyfile(src, dst)

print("--------------------------------------------------------")
print("********************************************************")

hasya=int(input("how much you have GPIO input?"))
masya=int(input("how much you have GPIO output?"))
number_of_PWM=int(input("How much you have PWM output?"))
number_of_ADC=int(input("How much ADC input exist?"))
number_of_UART=int(input("How much UART input exist?"))
#GPIO output of stm
 #GPIO input of stm
c=[["TIM2","2","A","15"],["TIM3","3","A","6"],["TIM4","4","D","12"],["TIM5","5","A","0"]]
f= open("main.c","w+")
f.write("//Header area\n")
f.write('#include "stm32f4xx_hal.h"\n')
f.write('/* Private typedef */\n')
f.write('/* Private define */\n')
f.write('/* Private macro */\n')
f.write('/* Private variables */\n')
f.write("//Function prototype area\n")
f.write("//Function without protype\n")

f.write("void Init_OnBoard(void){\n")
f.write(" GPIO_InitTypeDef GPIO_InitStruct = {0};\n")
f.write("//Configure GPIO\n")
f.write("__HAL_RCC_GPIOD_CLK_ENABLE();\n")
f.write("GPIO_InitStruct.Pin = GPIO_PIN_12;\n")
f.write("GPIO_InitStruct.Mode = GPIO_MODE_OUTPUT_PP;\n")
f.write("GPIO_InitStruct.Pull = GPIO_NOPULL;\n")
f.write("GPIO_InitStruct.Speed = GPIO_SPEED_FREQ_LOW;\n")
f.write("HAL_GPIO_Init(GPIOD, &GPIO_InitStruct);\n")

f.write("GPIO_InitStruct.Pin = GPIO_PIN_13;\n")
f.write("GPIO_InitStruct.Mode = GPIO_MODE_OUTPUT_PP;\n")
f.write("GPIO_InitStruct.Pull = GPIO_NOPULL;\n")
f.write("GPIO_InitStruct.Speed = GPIO_SPEED_FREQ_LOW;\n")
f.write("HAL_GPIO_Init(GPIOD, &GPIO_InitStruct);\n")

f.write("GPIO_InitStruct.Pin = GPIO_PIN_14;\n")
f.write("GPIO_InitStruct.Mode = GPIO_MODE_OUTPUT_PP;\n")
f.write("GPIO_InitStruct.Pull = GPIO_NOPULL;\n")
f.write("GPIO_InitStruct.Speed = GPIO_SPEED_FREQ_LOW;\n")
f.write("HAL_GPIO_Init(GPIOD, &GPIO_InitStruct);\n")

f.write("GPIO_InitStruct.Pin = GPIO_PIN_15;\n")
f.write("GPIO_InitStruct.Mode = GPIO_MODE_OUTPUT_PP;\n")
f.write("GPIO_InitStruct.Pull = GPIO_NOPULL;\n")
f.write("GPIO_InitStruct.Speed = GPIO_SPEED_FREQ_LOW;\n")
f.write("HAL_GPIO_Init(GPIOD, &GPIO_InitStruct);\n")
f.write("}\n")

f.write('/* Private user code */\n')
f.write("int main(void)\n")
f.write("{\n")
f.write("//Inside of the main function\n")
f.write(" HAL_Init();\n")

f.write(" Init_OnBoard();\n")
f.write("//Function calling area\n")
f.write("/* USER CODE  */\n")
f.write("while(1)\n")
f.write("{\n")
f.write("//Inside of the infinite loop in main function\n")
f.write("//Before the infinite loop\n")
f.write("//Tester part\n")
f.write("if(error)\n")
f.write("{\n")
f.write("HAL_GPIO_WritePin(GPIOD, GPIO_PIN_12, GPIO_PIN_SET);\n")
f.write("HAL_GPIO_WritePin(GPIOD, GPIO_PIN_13, GPIO_PIN_SET);\n")
f.write("HAL_GPIO_WritePin(GPIOD, GPIO_PIN_14, GPIO_PIN_SET);\n")
f.write("HAL_GPIO_WritePin(GPIOD, GPIO_PIN_15, GPIO_PIN_SET);\n")
f.write("}\n")
f.write("else\n")
f.write("{\n")
f.write("HAL_GPIO_WritePin(GPIOD, GPIO_PIN_12, GPIO_PIN_SET);\n")
f.write("HAL_GPIO_WritePin(GPIOD, GPIO_PIN_13, GPIO_PIN_SET);\n")
f.write("HAL_GPIO_WritePin(GPIOD, GPIO_PIN_14, GPIO_PIN_SET);\n")
f.write("HAL_GPIO_WritePin(GPIOD, GPIO_PIN_15, GPIO_PIN_SET);\n")
f.write("}\n")
f.write("}\n")
f.write("//After the infinite loop\n")
f.write("}\n")
f.write("//After the main funciton\n")
f.write("//Function area\n")
f.write("//Timer config  area\n")
f.write("//Handler area\n")
f.write("void Error_Handler(void)\n")
f.write("{\n")
f.write("__disable_irq();\n")
f.write("while (1)\n")
f.write("  {\n")
f.write("}\n")
f.write("}\n")
f.close()

if hasya>0:
    GPIO_In(hasya)
if masya>0:
    GPIO_OUT(masya)
if number_of_ADC>0:
    DAC_Checker(number_of_ADC)
if number_of_UART>0:
    UART_node(number_of_UART)    
if number_of_PWM>0:
    PWM_checker(number_of_PWM)



match()
if len(errorsum)>0:
    sux=errorsum[0]+"==0"
    for element in errorsum[1:]:
        sux =sux+ "&&"+ element+"==0"  
    with open("main.c", "r") as in_file:
        buf = in_file.readlines()
    with open("main.c", "w") as out_file:
        for line in buf:
            if line == "if(error)\n":
                line= f"if({sux})\n"             
            out_file.write(line)
system_clock_config.clk()