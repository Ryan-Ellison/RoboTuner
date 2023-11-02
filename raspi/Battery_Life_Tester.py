from Motor import Motor
import random as rand
import time

def random_movement(hrs=3, log_min=5):
	motor = Motor()
	start = time.time()
	t_dif = 0
	f = open("Battery_Life_Log.txt", "a")
	while ((t_dif := (time.time()-start)) <= 3600 * hrs):
		motor.set_speed(int(rand.randrange(250, 1001)))
		if rand.choice([True, False]):
			motor.push(rand.random()*9 + 1)
		else:
			motor.pull(rand.random()*9 + 1)
			
		if (round(t_dif % (60 * log_min)) == 0 and t_dif/60 > log_min/2):
			f.write(f"Still on and working at {t_dif/60} minutes\n")
			time.sleep(0.1)
	
	f.write(f"\nCompleted Battery Life Testing at {t_dif/60} minutes\n")
	f.close()
	
if __name__ == "__main__":
	random_movement(1/30, 0.5)
