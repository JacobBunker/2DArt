#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <assert.h>
#include <bsd/stdlib.h>
#include <time.h>
#include <math.h>
#include <float.h>
#include <limits.h>
#include <unistd.h>

#include <chipmunk.h>

#include <GL/glew.h>
#include <GL/glut.h>
#include <GLFW/glfw3.h>

#include <pthread.h>

#include "econ_simulator.h"

#define pi 3.1415926
#define NUM_NODES 100000
#define CLEAR_BUFFER 1
#define DRAW_POINTS 100000
#define DRAW_LINES 0

SimulationState render_sim;

char *name;
char buffer[64];
cpVect spawns[NUM_NODES];

void InitSim(SimulationState *sim) {
	sim->timeStep = 1.0 / (60.0 * 1.0);
	sim->render = 1;
	sim->arena_time_max = 20.0;

	sim->players = malloc(sizeof(Player) * NUM_NODES);

	for(int i = 0; i < NUM_NODES; ++i) {
		sim->players[i].a = ((float)(rand() % 100000) - 50000) * 0.00015;
		sim->players[i].b = ((float)(rand() % 2000) - 1000) * 0.01;
		sim->players[i].c = ((float)(rand() % 100000) - 50000) * 0.00015;
		sim->players[i].d = ((float)(rand() % 2000) - 1000) * 0.01;
	}
}

void FreeSim(SimulationState *sim) {
	free(sim->players);
}

void init(void)
{
	glClearColor(0.0, 0.0, 0.0, 0.0);
	glColor3f(0.0, 0.0, 1.0);
	glMatrixMode(GL_PROJECTION);	
	glLoadIdentity();
	glOrtho(-1000.0, 1000.0, -1000.0, 1000.0, -1.0, 1.0);

	glEnable(GL_POINT_SMOOTH);
	glHint(GL_POINT_SMOOTH_HINT, GL_NICEST);
	glEnable(GL_BLEND);

}
  
void timer( int value )
{
    glutTimerFunc(0.01, timer, 0 );
    glutPostRedisplay();
}

//takes [-1.0,1.0] value and change value and returns corresponding radian value between -pi and pi
float angle_helper(float angle, float change) { 
	if(angle + change < -1.0) {
		return angle_helper(angle + change + 2.0, 0.0);
	} else if (angle + change > 1.0) {
		return angle_helper(angle + change - 2.0, 0.0);
	} else {
		return (pi * (angle + change));
	}
}

void DrawLookLine(float x1, float y1, float x2, float y2) {
	glColor4f(1.0f, 1.0f, 0.0f, 0.3f);
	glBegin(GL_LINES);   
	glVertex3f(x1,y1,0.0);     
	glVertex3f(x2,y2,0.0);
	glEnd();
}

void DrawShootLine(float x1, float y1, float x2, float y2) {
	glColor3f(1.0f, 0.0f, 0.0f);
	glBegin(GL_LINES);   
	glVertex3f(x1,y1,0.0);     
	glVertex3f(x2,y2,0.0);
	glEnd();
}

void ResetSim(SimulationState *sim) {
	sim->time = 0.0;
}

void StepSim(SimulationState *sim, int graphics_on) {
	sim->players[0].pos = cpv(0.0 + (sim->players[0].a * sin(sim->players[0].b * sim->time)),
							 (0.0 + (sim->players[0].c * cos(sim->players[0].d * sim->time))));
	if(graphics_on) {
		DrawLookLine(0.0, 0.0, sim->players[0].pos.x, sim->players[0].pos.y);
	}

	for(int i = 1; i < NUM_NODES; ++i) {
		sim->players[i].pos = cpv(sim->players[i-1].pos.x + (sim->players[i].a * sin(sim->players[i].b * sim->time)),
								 (sim->players[i-1].pos.y + (sim->players[i].c * cos(sim->players[i].d * sim->time))));
		if(graphics_on) {
			DrawLookLine(sim->players[i-1].pos.x, sim->players[i-1].pos.y, sim->players[i].pos.x, sim->players[i].pos.y);
		}
	}
}

void display(void)
{
	if(CLEAR_BUFFER) {
		glClear(GL_COLOR_BUFFER_BIT);
	}
	glColor3f(1.0f, 1.0f, 0.0f);
	//glBegin(GL_LINES);   
	if(1) {//render_sim.time < render_sim.arena_time_max) {
		StepSim(&render_sim, DRAW_LINES);
		render_sim.time += render_sim.timeStep;

		//sleep(sim.timeStep);
		snprintf(buffer, sizeof buffer, "%f", render_sim.time);
		glutSetWindowTitle(buffer);

		glPointSize(1.0);
		glBegin(GL_POINTS);
		glColor3f(1.0f, 0.0f, 0.0f);

		if(DRAW_POINTS) {
			glVertex3f(0.0f, 0.0f, 0.0f);

			for(int i = NUM_NODES - DRAW_POINTS; i < NUM_NODES; ++i) {
				glVertex3f(render_sim.players[i].pos.x, render_sim.players[i].pos.y, 0.0f);
				//glColor3f(1.0f, 0.0f, 0.0f);
				//printf("%d %f %f\n", i, render_sim.players[i].pos.x, render_sim.players[i].pos.y);
			}
		} else {
			glVertex3f(render_sim.players[NUM_NODES - 1].pos.x, render_sim.players[NUM_NODES - 1].pos.y, 0.0f);
		}

		glEnd(); 
		glutSwapBuffers();

	} else if(render_sim.render == 1){
		char *name = "SIMULATION ENDED";
		glutSetWindowTitle(name);
		ResetSim(&render_sim);
	}  
}


int main(int argc, char** argv) {
	srand(time(0));
	InitSim(&render_sim);

	glutInit(&argc, argv);
	glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB);
	glutInitWindowSize(800, 800);
	glutInitWindowPosition(100, 100);
	glutCreateWindow("Simulator");
	init();
	glutTimerFunc(0, timer, 0);
	glutDisplayFunc(display);
	glutMainLoop();

	return 0;
}
