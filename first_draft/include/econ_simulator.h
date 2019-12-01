#ifndef econ_simulator_H
#define econ_simulator_H

typedef struct {
	int id;
	cpVect pos;
	//cpVect vel;
	float a, b, c, d;
} Player;

typedef struct {
	Player *players;

	cpFloat timeStep;
	cpFloat arena_time_max;
	cpVect target;
	float t_s_dist;

	float time;
	int render;

} SimulationState;

#endif

