import threading, time, sys, signal, math, os, RPIO
import RPi.GPIO as GPIO
from RPIO import PWM	

GPIO.setmode(GPIO.BCM)
RPIO.setup(17, RPIO.IN)
RPIO.setup(17, RPIO.IN, pull_up_down=RPIO.PUD_UP)
RPIO.setup(22, RPIO.IN)
RPIO.setup(22, RPIO.IN, pull_up_down=RPIO.PUD_UP)
RPIO.setwarnings(False)
RPIO.setup(24, RPIO.IN)
RPIO.setup(24, RPIO.IN, pull_up_down=RPIO.PUD_UP)
RPIO.setup(25, RPIO.IN)
RPIO.setup(25, RPIO.IN, pull_up_down=RPIO.PUD_UP)

running = True


# Funcion que activa los servos correspondientes para recoger y soltar las pelotas de tenis
def accion_servo(servo_mover):

	servo = PWM.Servo()
	#activamos servo delantero para recoger pelotas (sube 90 - 40 grados evitar choque varilla delantera suelo)
	if (servo_mover == 'D'):
		servo.set_servo(27, 2500) 
		time.sleep(2)
		servo.set_servo(27, 1100) 
		time.sleep(1)
		servo.stop_servo(27)
		RPIO.setup(27, RPIO.IN)
	#activamos servo trasero para soltar las pelotas ( 54 - 4 grados aprox)
	else:
		servo.set_servo(23, 1500) 
		time.sleep(1)
		servo.set_servo(23, 100)
		time.sleep(1)
		servo.stop_servo(23)
		RPIO.setup(23, RPIO.IN)

# Funcion que hace girar los motores hacia adelante
def adelante():

	global contador1
	global contador2

	anterior_izq_A=RPIO.input(17)
  	anterior_izq_B=RPIO.input(22)

 	anterior_der_A=RPIO.input(24)
  	anterior_der_B=RPIO.input(25)

  	while running:

    		input_value_17 = RPIO.input(17)
    		input_value_22 = RPIO.input(22)


    		if (input_value_17 != anterior_izq_A or input_value_22 != anterior_izq_B):
			# IZQ = 0  DER = 0 
			if (anterior_izq_A == False and anterior_izq_B == False):
				# SIG_IZQ = 1 SIG_DER = 0
				if (input_value_17 == True and input_value_22 == False):
                			contador1 = contador1 + 1

				# SIG_IZQ = 1 SIG_DER = 1
				elif (input_value_17 == True and input_value_22 == True):
					contador1 = contador1 + 2

				# SIG_IZQ = 0 SIG_DER = 1 
				elif (input_value_17 == False and input_value_22 == True):
					contador1 = contador1 + 3

        		# IZQ = 0    DER = 1
    			elif (anterior_izq_A== False and anterior_izq_B == True):

				# SIG_IZQ = 0 SIG_DER = 0
				if (input_value_17 == False and input_value_22 == False):
                        		contador1 = contador1 + 1

				# SIG_IZQ = 1 SIG_DER = 0
				elif (input_value_17 == True and input_value_22 == False):
                        		contador1 = contador1 + 2

				# SIG_IZQ = 1 SIG_DER = 1
				elif (input_value_17 == True and input_value_22 == True):
                        		contador1 = contador1 + 3

        		# IZQ = 1    DER = 0
    			elif (anterior_izq_A== True and anterior_izq_B == False):

				# SIG_IZQ = 1 SIG_DER = 1
				if (input_value_17 == True and input_value_22 == True):
                        		contador1 = contador1 + 1

				# SIG_IZQ = 0 SIG_DER = 1
				elif (input_value_17 == False  and input_value_22 == True):
                        		contador1 = contador1 + 2

				# SIG_IZQ = 0 SIG_DER = 0
				elif (input_value_17 == False and input_value_22 == False):
                        		contador1 = contador1 + 3

        		# IZQ = 1    DER = 1 
    			elif (anterior_izq_A== True and anterior_izq_B == True):

				# SIG_IZQ = 0 SIG_DER = 1 
				if (input_value_17 == False and input_value_22 == True):
                        		contador1 = contador1 + 1
		
				# SIG_IZQ = 0 SIG_DER = 0
				elif (input_value_17 == False  and input_value_22 == False):
                        		contador1 = contador1 + 2

				# SIG_IZQ = 1 SIG_DER = 0
				elif (input_value_17 == True and input_value_22 == False):
                        		contador1 = contador1 + 3

        	anterior_izq_A = input_value_17
        	anterior_izq_B = input_value_22
	
		# MOTOR DERECHO

    		input_value_24 = RPIO.input(24)
    		input_value_25 = RPIO.input(25)

    		if (input_value_24 != anterior_der_A or input_value_25 != anterior_der_B):
			#  IZQ = 0  DER = 0 
			if (anterior_der_A == False and anterior_der_B == False):

				# SIG_IZQ = 1 SIG_DER = 0
				if (input_value_24 == True and input_value_25 == False):
                			contador2 = contador2 + 1
						
				# SIG_IZQ = 1 SIG_DER = 1
				elif (input_value_24 == True and input_value_25 == True):
					contador2 = contador2 + 2

				# SIG_IZQ = 0 SIG_DER = 1
				elif (input_value_24 == False and input_value_25 == True):
					contador2 = contador2 + 3

        		# IZQ = 0    DER = 1
    			elif (anterior_der_A== False and anterior_der_B == True):

				# SIG_IZQ = 0 SIG_DER = 1
				if (input_value_24 == False and input_value_25 == False):
                        		contador2 = contador2 + 1
			
				# SIG_IZQ = 1 SIG_DER = 0
				elif (input_value_24 == True and input_value_25 == False):
                        		contador2 = contador2 + 2

				# SIG_IZQ = 1 SIG_DER = 1
				elif (input_value_24 == True and input_value_25 == True):
                        		contador2 = contador2 + 3

        		# IZQ = 1    DER = 0
    			elif (anterior_der_A== True and anterior_der_B == False):

				# SIG_IZQ = 1 SIG_DER = 1
				if (input_value_24 == True and input_value_25 == True):
                        		contador2 = contador2 + 1

				# SIG_IZQ = 0 SIG_DER = 1
				elif (input_value_24 == False  and input_value_25 == True):
                        		contador2 = contador2 + 2

				# SIG_IZQ = 0 SIG_DER = 0			
				elif (input_value_24 == False and input_value_25 == False):
                        		contador2 = contador2 + 3

        		# IZQ = 1    DER = 1 
    			elif (anterior_der_A== True and anterior_der_B == True): 
			
				# SIG_IZQ = 0 SIG_DER = 1
				if (input_value_24 == False and input_value_25 == True):
                        		contador2 = contador2 + 1
		
				# SIG_IZQ = 0 SIG_DER = 0
				elif (input_value_24 == False  and input_value_25 == False):
                        		contador2 = contador2 + 2

				# SIG_IZQ = 1 SIG_DER = 0 
				elif (input_value_24 == True and input_value_25 == False):
                        		contador2 = contador2 + 3

        	
		anterior_der_A = input_value_24
        	anterior_der_B = input_value_25
		
	#END_WHILE
	hilo.stopped = True
        return([contador1, contador2])
 


# Funcion que hace girar los motores hacia detras
def atras():

	global contador1
	global contador2

	anterior_izq_A=RPIO.input(17)
  	anterior_izq_B=RPIO.input(22)

 	anterior_der_A=RPIO.input(24)
  	anterior_der_B=RPIO.input(25)

  	while running:

    		input_value_17 = RPIO.input(17)
    		input_value_22 = RPIO.input(22)

    		if (input_value_17 != anterior_izq_A or input_value_22 != anterior_izq_B):
       		
			# IZQ = 0  DER = 0 
			if (anterior_izq_A == False and anterior_izq_B == False):

				# SIG_IZQ = 1 SIG_DER = 0
				if (input_value_17 == True and input_value_22 == False):
                			contador1 = contador1 - 3

				# SIG_IZQ = 1 SIG_DER = 1
				elif (input_value_17 == True and input_value_22 == True):
					contador1 = contador1 - 2

				# SIG_IZQ = 0 SIG_DER = 
				elif (input_value_17 == False and input_value_22 == True):
					contador1 = contador1 - 1

        		# IZQ = 0    DER = 1
    			elif (anterior_izq_A== False and anterior_izq_B == True):

				# SIG_IZQ = 0 SIG_DER = 0
				if (input_value_17 == False and input_value_22 == False):
                        		contador1 = contador1 - 3

				# SIG_IZQ = 1 SIG_DER = 0
				elif (input_value_17 == True and input_value_22 == False):
                        		contador1 = contador1 - 2

				# SIG_IZQ = 1 SIG_DER = 1
				elif (input_value_17 == True and input_value_22 == True):
                        		contador1 = contador1 - 1

        		# IZQ = 1    DER = 0
    			elif (anterior_izq_A== True and anterior_izq_B == False):

				# SIG_IZQ = 1 SIG_DER = 1
				if (input_value_17 == True and input_value_22 == True):
                        		contador1 = contador1 - 3

				# SIG_IZQ = 0 SIG_DER = 1
				elif (input_value_17 == False  and input_value_22 == True):
                        		contador1 = contador1 - 2

				# SIG_IZQ = 0 SIG_DER = 0
				elif (input_value_17 == False and input_value_22 == False):
                        		contador1 = contador1 - 1

        		# IZQ = 1    DER = 1 
    			elif (anterior_izq_A== True and anterior_izq_B == True):

				# SIG_IZQ = 0 SIG_DER = 1 
				if (input_value_17 == False and input_value_22 == True):
                        		contador1 = contador1 - 3 
		
				# SIG_IZQ = 0 SIG_DER = 0
				elif (input_value_17 == False  and input_value_22 == False):
                        		contador1 = contador1 - 2

				# SIG_IZQ = 1 SIG_DER = 0
				elif (input_value_17 == True and input_value_22 == False):
                        		contador1 = contador1 - 1

        	anterior_izq_A = input_value_17
        	anterior_izq_B = input_value_22
	
		# MOTOR DERECHO

    		input_value_24 = RPIO.input(24)
    		input_value_25 = RPIO.input(25)

    		if (input_value_24 != anterior_der_A or input_value_25 != anterior_der_B):
			#  IZQ = 0  DER = 0 
			if (anterior_der_A == False and anterior_der_B == False):

				# SIG_IZQ = 1 SIG_DER = 0
				if (input_value_24 == True and input_value_25 == False):
                			contador2 = contador2 - 3

				# SIG_IZQ = 1 SIG_DER = 1
				elif (input_value_24 == True and input_value_25 == True):
					contador2 = contador2 - 2

				# SIG_IZQ = 0 SIG_DER = 1
				elif (input_value_24 == False and input_value_25 == True):
					contador2 = contador2 - 1

        		# IZQ = 0    DER = 1
    			elif (anterior_der_A== False and anterior_der_B == True):

				# SIG_IZQ = 0 SIG_DER = 1
				if (input_value_24 == False and input_value_25 == False):
                        		contador2 = contador2 - 3
			
				# SIG_IZQ = 1 SIG_DER = 0
				elif (input_value_24 == True and input_value_25 == False):
                        		contador2 = contador2 - 2

				# SIG_IZQ = 1 SIG_DER = 1
				elif (input_value_24 == True and input_value_25 == True):
                        		contador2 = contador2 - 1

        		# IZQ = 1    DER = 0
    			elif (anterior_der_A== True and anterior_der_B == False):

				# SIG_IZQ = 1 SIG_DER = 1
				if (input_value_24 == True and input_value_25 == True):
                        		contador2 = contador2 - 3

				# SIG_IZQ = 0 SIG_DER = 1
				elif (input_value_24 == False  and input_value_25 == True):
                        		contador2 = contador2 - 2

				# SIG_IZQ = 0 SIG_DER = 0			
				elif (input_value_24 == False and input_value_25 == False):
                        		contador2 = contador2 - 1

        		# IZQ = 1    DER = 1 
    			elif (anterior_der_A== True and anterior_der_B == True): 
			
				# SIG_IZQ = 0 SIG_DER = 1
				if (input_value_24 == False and input_value_25 == True):
                        		contador2 = contador2 - 3
		
				# SIG_IZQ = 0 SIG_DER = 0
				elif (input_value_24 == False  and input_value_25 == False):
                        		contador2 = contador2 - 2

				# SIG_IZQ = 1 SIG_DER = 0 
				elif (input_value_24 == True and input_value_25 == False):
                        		contador2 = contador2 - 1

        	anterior_der_A = input_value_24
        	anterior_der_B = input_value_25
    
	#END_WHILE
	hilo.stopped = True
        return([contador1,contador2])


# Funcion que realiza el giro del robot
def giro():


	global contador1
	global contador2
	global sentido

	
	if (sentido == 'IZQUIERDA'):

		#ENCODER IZQUIERDO
		anterior_izq_A=RPIO.input(17)
  		anterior_izq_B=RPIO.input(22)

  		#ENCODER DERECHO
 		anterior_der_A=RPIO.input(24)
  		anterior_der_B=RPIO.input(25)	


  		while running:
			# MOTOR IZQUIERDO ATRAS
			input_value_17 = RPIO.input(17)
    			input_value_22 = RPIO.input(22)

    			if (input_value_17 != anterior_izq_A or input_value_22 != anterior_izq_B):
       		
				# IZQ = 0  DER = 0 
				if (anterior_izq_A == False and anterior_izq_B == False):

					# SIG_IZQ = 1 SIG_DER = 0
					if (input_value_17 == True and input_value_22 == False):
                				contador1 = contador1 - 3

					# SIG_IZQ = 1 SIG_DER = 1
					elif (input_value_17 == True and input_value_22 == True):
						contador1 = contador1 - 2

					# SIG_IZQ = 0 SIG_DER = 1
					elif (input_value_17 == False and input_value_22 == True):
						contador1 = contador1 - 1

        			# IZQ = 0    DER = 1
    				elif (anterior_izq_A== False and anterior_izq_B == True):

						# SIG_IZQ = 0 SIG_DER = 0
					if (input_value_17 == False and input_value_22 == False):
                        			contador1 = contador1 - 3

					# SIG_IZQ = 1 SIG_DER = 0
					elif (input_value_17 == True and input_value_22 == False):
                        			contador1 = contador1 - 2

					# SIG_IZQ = 1 SIG_DER = 1
					elif (input_value_17 == True and input_value_22 == True):
                        			contador1 = contador1 - 1

        			# IZQ = 1    DER = 0
    				elif (anterior_izq_A== True and anterior_izq_B == False):

					# SIG_IZQ = 1 SIG_DER = 1
					if (input_value_17 == True and input_value_22 == True):
                        			contador1 = contador1 - 3

					# SIG_IZQ = 0 SIG_DER = 1
					elif (input_value_17 == False  and input_value_22 == True):
                        			contador1 = contador1 - 2

					# SIG_IZQ = 0 SIG_DER = 0
					elif (input_value_17 == False and input_value_22 == False):
                        			contador1 = contador1 - 1

        			# IZQ = 1    DER = 1 
    				elif (anterior_izq_A== True and anterior_izq_B == True):

					# SIG_IZQ = 0 SIG_DER = 1 
					if (input_value_17 == False and input_value_22 == True):
                        			contador1 = contador1 - 3 
		
					# SIG_IZQ = 0 SIG_DER = 0
					elif (input_value_17 == False  and input_value_22 == False):
                        			contador1 = contador1 - 2

					# SIG_IZQ = 1 SIG_DER = 0
					elif (input_value_17 == True and input_value_22 == False):
                        			contador1 = contador1 - 1

        		anterior_izq_A = input_value_17
        		anterior_izq_B = input_value_22
    		
			
			# MOTOR DERECHO ADELANTE
			input_value_24 = RPIO.input(24)
    			input_value_25 = RPIO.input(25)

    			if (input_value_24 != anterior_der_A or input_value_25 != anterior_der_B):
				#  IZQ = 0  DER = 0 
				if (anterior_der_A == False and anterior_der_B == False):

					# SIG_IZQ = 1 SIG_DER = 0
					if (input_value_24 == True and input_value_25 == False):
                				contador2 = contador2 + 1

					# SIG_IZQ = 1 SIG_DER = 1
					elif (input_value_24 == True and input_value_25 == True):
						contador2 = contador2 + 2

					# SIG_IZQ = 0 SIG_DER = 1
					elif (input_value_24 == False and input_value_25 == True):
						contador2 = contador2 + 3

        			# IZQ = 0    DER = 1
    				elif (anterior_der_A== False and anterior_der_B == True):

					# SIG_IZQ = 0 SIG_DER = 1
					if (input_value_24 == False and input_value_25 == False):
                        			contador2 = contador2 + 1
			
					# SIG_IZQ = 1 SIG_DER = 0
					elif (input_value_24 == True and input_value_25 == False):
                        			contador2 = contador2 + 2

					# SIG_IZQ = 1 SIG_DER = 1
					elif (input_value_24 == True and input_value_25 == True):
                        			contador2 = contador2 + 3

        			# IZQ = 1    DER = 0
    				elif (anterior_der_A== True and anterior_der_B == False):

					# SIG_IZQ = 1 SIG_DER = 1
					if (input_value_24 == True and input_value_25 == True):
                        			contador2 = contador2 + 1

					# SIG_IZQ = 0 SIG_DER = 1
					elif (input_value_24 == False  and input_value_25 == True):
                        			contador2 = contador2 + 2

					# SIG_IZQ = 0 SIG_DER = 0			
					elif (input_value_24 == False and input_value_25 == False):
                        			contador2 = contador2 + 3

        			# IZQ = 1    DER = 1 
    				elif (anterior_der_A== True and anterior_der_B == True): 
			
					# SIG_IZQ = 0 SIG_DER = 1
					if (input_value_24 == False and input_value_25 == True):
                        			contador2 = contador2 + 1
		
					# SIG_IZQ = 0 SIG_DER = 0
					elif (input_value_24 == False  and input_value_25 == False):
                        			contador2 = contador2 + 2

					# SIG_IZQ = 1 SIG_DER = 0 
					elif (input_value_24 == True and input_value_25 == False):
                        			contador2 = contador2 + 3

        		anterior_der_A = input_value_24
        		anterior_der_B = input_value_25
	
		#END_WHILE
	
		hilo.stopped = True		

	#END_IF



	#Giramos a la derecha (IZQ-Atras, DER-Adelante)
	else:

		anterior_izq_A=RPIO.input(17)
  		anterior_izq_B=RPIO.input(22)

 		anterior_der_A=RPIO.input(24)
  		anterior_der_B=RPIO.input(25)

  		while running:
			# MOTOR IZQUIERDO ADELANTE
			input_value_17 = RPIO.input(17)
    			input_value_22 = RPIO.input(22)

    			if (input_value_17 != anterior_izq_A or input_value_22 != anterior_izq_B):
       		
				# IZQ = 0  DER = 0 
				if (anterior_izq_A == False and anterior_izq_B == False):

					# SIG_IZQ = 1 SIG_DER = 0
					if (input_value_17 == True and input_value_22 == False):
                				contador1 = contador1 + 1

					# SIG_IZQ = 1 SIG_DER = 1
					elif (input_value_17 == True and input_value_22 == True):
						contador1 = contador1 + 2

					# SIG_IZQ = 0 SIG_DER = 1
					elif (input_value_17 == False and input_value_22 == True):
						contador1 = contador1 + 3

        			# IZQ = 0    DER = 1
    				elif (anterior_izq_A== False and anterior_izq_B == True):

					# SIG_IZQ = 0 SIG_DER = 0
					if (input_value_17 == False and input_value_22 == False):
                        			contador1 = contador1 + 1

					# SIG_IZQ = 1 SIG_DER = 0
					elif (input_value_17 == True and input_value_22 == False):
                        			contador1 = contador1 + 2

					# SIG_IZQ = 1 SIG_DER = 1
					elif (input_value_17 == True and input_value_22 == True):
                        			contador1 = contador1 + 3

        			# IZQ = 1    DER = 0
    				elif (anterior_izq_A== True and anterior_izq_B == False):

					# SIG_IZQ = 1 SIG_DER = 1
					if (input_value_17 == True and input_value_22 == True):
                        			contador1 = contador1 + 1

					# SIG_IZQ = 0 SIG_DER = 1
					elif (input_value_17 == False  and input_value_22 == True):
                        			contador1 = contador1 + 2

					# SIG_IZQ = 0 SIG_DER = 0
					elif (input_value_17 == False and input_value_22 == False):
                        			contador1 = contador1 + 3

        			# IZQ = 1    DER = 1 
    				elif (anterior_izq_A== True and anterior_izq_B == True):

					# SIG_IZQ = 0 SIG_DER = 1 
					if (input_value_17 == False and input_value_22 == True):
                        			contador1 = contador1 + 1
		
					# SIG_IZQ = 0 SIG_DER = 0
					elif (input_value_17 == False  and input_value_22 == False):
                        			contador1 = contador1 + 2

					# SIG_IZQ = 1 SIG_DER = 0
					elif (input_value_17 == True and input_value_22 == False):
                        			contador1 = contador1 + 3

        		anterior_izq_A = input_value_17
        		anterior_izq_B = input_value_22
    			

			# MOTOR DERECHO ATRAS

    			input_value_24 = RPIO.input(24)
    			input_value_25 = RPIO.input(25)

    			if (input_value_24 != anterior_der_A or input_value_25 != anterior_der_B):
				#  IZQ = 0  DER = 0 
				if (anterior_der_A == False and anterior_der_B == False):

					# SIG_IZQ = 1 SIG_DER = 0
					if (input_value_24 == True and input_value_25 == False):
                				contador2 = contador2 - 3

					# SIG_IZQ = 1 SIG_DER = 1
					elif (input_value_24 == True and input_value_25 == True):
						contador2 = contador2 - 2

					# SIG_IZQ = 0 SIG_DER = 1
					elif (input_value_24 == False and input_value_25 == True):
						contador2 = contador2 - 1

        			# IZQ = 0    DER = 1
    				elif (anterior_der_A== False and anterior_der_B == True):

					# SIG_IZQ = 0 SIG_DER = 1
					if (input_value_24 == False and input_value_25 == False):
                        			contador2 = contador2 - 3
			
					# SIG_IZQ = 1 SIG_DER = 0
					elif (input_value_24 == True and input_value_25 == False):
                        			contador2 = contador2 - 2

					# SIG_IZQ = 1 SIG_DER = 1
					elif (input_value_24 == True and input_value_25 == True):
                        			contador2 = contador2 - 1

        			# IZQ = 1    DER = 0
    				elif (anterior_der_A== True and anterior_der_B == False):

					# SIG_IZQ = 1 SIG_DER = 1
					if (input_value_24 == True and input_value_25 == True):
                        			contador2 = contador2 - 3

					# SIG_IZQ = 0 SIG_DER = 1
					elif (input_value_24 == False  and input_value_25 == True):
                        			contador2 = contador2 - 2

					# SIG_IZQ = 0 SIG_DER = 0			
					elif (input_value_24 == False and input_value_25 == False):
                        			contador2 = contador2 - 1

        			# IZQ = 1    DER = 1 
    				elif (anterior_der_A== True and anterior_der_B == True): 
			
					# SIG_IZQ = 0 SIG_DER = 1
					if (input_value_24 == False and input_value_25 == True):
                        			contador2 = contador2 - 3
		
					# SIG_IZQ = 0 SIG_DER = 0
					elif (input_value_24 == False  and input_value_25 == False):
                        			contador2 = contador2 - 2

					# SIG_IZQ = 1 SIG_DER = 0 
					elif (input_value_24 == True and input_value_25 == False):
                        			contador2 = contador2 - 1

        		anterior_der_A = input_value_24
        		anterior_der_B = input_value_25


		#END_WHILE			
		hilo.stopped = True

	#END_ELSE

	return ([contador1, contador2])
	
# HILO encargado de realizar el sistema de control proporcional integral, calcular el numero de ticks
def monitor(tid, itemID=None, threshold=None):
	global running
	global sentido

	# NUMERO DE TICKS. 
	centimetros = int(sys.argv[2])
	if (sentido == "ADELANTE") or (sentido == "ATRAS"):
		num_ticks_der = (TOTAL_TICKS_VUELTA_DER * centimetros)/dos_pi_R
		num_ticks_izq = ((TOTAL_TICKS_VUELTA_IZQ + tolerancia) * centimetros)/dos_pi_R
		#print ("Numero de ticks izq es -> %s") % num_ticks_izq 
		#print ("Numero de ticks der es -> %s") % num_ticks_der
	#SI GIRA DERECHA o IZQUIERDA
	elif (sentido == "DERECHA") or (sentido == "IZQUIERDA"):
		num_ticks_izq = centimetros * TICKS_POR_GRADO_IZQ * 2
		num_ticks_der = centimetros * TICKS_POR_GRADO_DER * 2
		num_ticks_izq = (num_ticks_izq )   + tolerancia 
		num_ticks_der = (num_ticks_der )  

	cont_aux = 0

	tole_error = 2
	T = 0.05

	ukm1_der = 0.0
	ukm1_izq = 0.0
	ekm1_d = 0.0
	ekm1_i = 0.0
	
	#VALORES A KsuP y KsuI para conseguir movimiento
	kp = 0.75
	ki = 0.01 * kp

	p0 = (ki * T/2) + kp
	p1 = (ki * T/2) - kp

	#print "kp =%s, ki=%s, p0=%s, p1=%s" % (kp,ki,p0,p1)

	#MOTOR IZQUIERDO = Motor1
	#MOTOR DERECHO = Motor2	
	if (sentido == "ADELANTE"):
		#print "ADELANTE"
		Motor1 = 28
		Motor2 = 29
		
	elif (sentido == "ATRAS"):
		#print "ATRAS"
		Motor1 = 30
		Motor2 = 31

	elif (sentido == "IZQUIERDA"):
		#print "GIRO_IZQUIERDA"
		Motor1 = 30
		Motor2 = 29	
	else:
		#print "GIRO_DERECHA"
		Motor1 = 28
		Motor2 = 31
	
	GPIO.setup(Motor1, GPIO.OUT)
	p_izq = GPIO.PWM(Motor1, 100)
	p_izq.start(0)

	GPIO.setup(Motor2, GPIO.OUT)
	p_der = GPIO.PWM(Motor2, 100)
	p_der.start(0)	

	freq_muestreo = T * 10000
	while running:
		cont_aux = cont_aux + 1
		if (math.fmod(cont_aux, int(freq_muestreo))  == 0):	

			ek_d = num_ticks_der - abs(contador2) 
			uk_d = ukm1_der + p0 * ek_d + p1 * ekm1_d
			ek_i = num_ticks_izq - abs(contador1)	
			uk_i = ukm1_izq + p0 * ek_i + p1 * ekm1_i

			uk_i_s = min(uk_i,100.0)
			uk_i_s = max(uk_i_s, 0.0)
			uk_d_s = min(uk_d,100.0)
			uk_d_s = max(uk_d_s, 0.0)

			uk_max = max(uk_i_s, uk_d_s)
			p_izq.ChangeDutyCycle(int(uk_max))
			p_der.ChangeDutyCycle(int(uk_max))
	        	#print "ek_i = %s, uk_i = %s, ek_d= %s, uk_d= %s" % (ek_i, uk_i, ek_d, uk_d)
			#print "---------------------------------------------------------------------------------------"
			#print "ek_d = %s, uk_d = %s, ekm1_d=%s, ukm1_der = %s" % (ek_d, uk_d, ekm1_d, ukm1_der)
			#print "======================================================================================="
						
			#PARA EL GIRO la condicion de parada distinta
			if (sentido == "IZQUIERDA") or (sentido == "DERECHA"):
				if (max(ek_i, ek_d) < tole_error):
					p_der.stop()
					p_izq.stop()
					GPIO.cleanup()
					break

			elif (sentido == "ADELANTE") or (sentido == "ATRAS"):
				if (abs(ek_i) < tole_error) or (abs(ek_d) < tole_error):
					p_der.stop()
					p_izq.stop()
					GPIO.cleanup()
					break			

			#actualizamos variables
			ukm1_der = uk_d
			ukm1_izq = uk_i

			ekm1_d = ek_d
			ekm1_i = ek_i
	
	#print "ek_i = %s, uk_i = %s, ek_d= %s, uk_d= %s" % (ek_i, uk_i, ek_d, uk_d)
	hilo2.stopped =True
	running = False
	#end_WHILE

#SEGUNDO HILO para actualizar los contadores llamando al movimiento detras, delante o giro
def actualizo_contador(tid, itemID=None, threshold=None):	
	global sentido
	global contador1
	contador1 = 0
	global contador2
	contador2 = 0

	global PI
	PI = 3.14

	global dos_pi_R
	dos_pi_R = 34.5575
	
	global TOTAL_TICKS_VUELTA_IZQ 
	TOTAL_TICKS_VUELTA_IZQ = 86
	global TOTAL_TICKS_VUELTA_DER 
	TOTAL_TICKS_VUELTA_DER = 89
	
	global tolerancia
	tolerancia = abs(TOTAL_TICKS_VUELTA_DER - TOTAL_TICKS_VUELTA_IZQ) 

	global TICKS_POR_GRADO_IZQ 
	TICKS_POR_GRADO_IZQ = 0.3752 * 2

	global TICKS_POR_GRADO_DER
	TICKS_POR_GRADO_DER = 0.3883 * 2

	if (sys.argv[1] == 'F'):
		sentido = "ADELANTE"
		resultados = adelante()

	elif (sys.argv[1] == 'B'):
		sentido = "ATRAS"
		resultados = atras()
		#servo = 'D'
		#accion_servo(servo)
  
	elif (sys.argv[1] == 'L' or sys.argv[1] == 'R'):
		sentido = "IZQUIERDA"	
		if (sys.argv[1] == 'R'):
			sentido = "DERECHA"	
		resultados = giro()
 
	RPIO.cleanup()	
	print (resultados)


def _handle_signal(signal, frame):
	global running	
	running = False
         
if __name__ == '__main__':
	signal.signal(signal.SIGTERM, _handle_signal)
	signal.signal(signal.SIGINT, _handle_signal)
	
hilo = threading.Thread(target=monitor, args=(1,), kwargs={'itemID':'1', 'threshold':60})
hilo2 = threading.Thread(target=actualizo_contador, args=(1,), kwargs={'itemID':'2', 'threshold':60})
hilo2.start()
hilo.start()
hilo.join(30)
hilo2.join(30)

