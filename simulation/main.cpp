#include <iostream>
#include <fstream>
#include <string>
#include <cstring>
#include <list>
#include "common.h"
#include "TissueVolume.h"
#include "tables.h"
using namespace std;
using namespace adevs;

/********************************************************************************
Basis Information:
The diameter of your esophagus is 24mm, the diameter of a quarter.
The thickness of your esophageal wall is 4mm, the width of 3 pennies.

We will use 24 mm in our simulation which gives the circumference to be 75.4 mm.
The grid width is 0.42 mm for ni = 179 or 0.21 mm for ni = 359.
Jumbo biopsy is about 5mmx3mm (12 by 7 grid) or (24 by 14 grid).

This model is based closely on the one appearing in

Kit Curtius, William D. Hazelton, Jihyoun Jeon, and E. Georg Luebeck (2015)
A Multiscale Model Evaluates Screening for Neoplasia in Barret's Esophagus
PLOS Computational Biology 11(5):e1004272. doi 10.1371/journal.pcbi.100472.

The essential operation of the model is as follows:

A grid of TissueVolume models is created. Each TissueVolume on the surface
of the esophagus section being looked at begins life with BE. Everything
below the surface is NORMAL.

At some point (possibly too far into the future to matter) some of the BE volumes
will mutate into DYSPLASIA. Then the DYSPLASIA volumes will mutate into CANCER.

The DYSPLASIA volumes will spread into other parts of the BE volume. The CANCER
volumes will spread into NORMAL and DYSPLASIA volumes.

The tumor grows via these two processes of mutation and growth. All of the
growth and mutation rules can be found in the TumorVolume class.

********************************************************************************/

#define NUM_LAYERS 5
// Fractional thickness of each layer
static const double LayerThicknessFraction[NUM_LAYERS] =
{
	0.2, // Epithelium
	0.1, // Basement membrane
	0.2, // Lamina propia
	0.1, // Mucular mucosaa
	0.4  // Submucosa
};

static const double grid_size = 0.42; // mm
static const double thickness = 4.0; // mm
static const double circumference = 75.4; // mm
static const double length = 250.0; // mm
static const int ni = (circumference / grid_size)+1; // Spatial points in X direction. 
static const int nj = (length / grid_size)+1; // Spatial points in Y direction. 
static const int nk = (thickness / grid_size)+1;	 // Spatial points in Z direction. 

// The TissueVolume objects in this CellSpace comprise the dynamic part of the model
static CellSpace<int>* tissue;
// The Simulator handles time management, etc.
static Simulator<CellEvent<int> >* sim;
// File for parameters not hard coded into the model.
static std::string inputData = "input.txt";
// Time points for taking biopsies
static list<double> biopsy;
// Onset age for be
static double be_onset=10000;
// Death age for tissue/patient
static double death_age=10000;
// Intervals
static double timeDysplasia = 10000;
static double timeCancer = 10000;
/**
 * Calculate the length of the BE segment in grid points.
 */
int calculate_be_length()
{
	const double long_be_prob = 0.25;
	const double long_be_mean = 6.4; // cm
	const double long_be_std_dev = 3.1; // cm
	const double short_be_mean = 1.4; // cm
	const double short_be_std_dev = 0.7; // cm
	double length;
	if (Parameters::getInstance()->uniform() < long_be_prob)
		length = Parameters::getInstance()->normal(long_be_mean,long_be_std_dev);
	else
		length = Parameters::getInstance()->normal(short_be_mean,short_be_std_dev);
	if (length < 0.47) length = 0.47;
	return (int(length*10.0/grid_size)+1);
}

/**
 * This data can be visualized using paraview. See 
 * www.paraview.org/Wiki/ParaView/Data_formats
 */
void PrintCSV(int seq_num, int rand, double t)
{
	assert(NUM_CELL_TYPES == 4);
	/*static const char* names[NUM_CELL_TYPES] = {
		"normal",
		"BE",
		"dysplasia",
		"cancer",
	};*/
	int types[NUM_CELL_TYPES] = { 0, 0, 0, 0 };
	char filename[100];
	sprintf(filename,"tumor.csv.%d.%d",seq_num,rand);
	// Output the paraview file format
	ofstream fout(filename);
	fout << "xcoord,ycoord,zcoord,type" << endl;
	for (int i = 0; i < ni; i++)
		for (int j = 0; j < nj; j++)
			for (int k = 0; k < nk; k++)
			{
				int type =
					dynamic_cast<TissueVolume*>(tissue->getModel(i,j,k))->itype();
				types[type]++;
				if (type >= BE)
				{
					fout << i << "," << j << "," << k << "," << type << endl;
				}
			}
	fout.close();
}
void PrintInterval(int seq_num, int rand, vector<double> hgds, vector<double> hgc)
{
	char file[100];
	sprintf(file,"intervals.csv.%d.%d",seq_num,rand);
	// Output intervals between first occurances of cancer and dysplasia
	ofstream fout1(file);
	fout1 << "onsetAge,deathAge,timeDysplasia,timeCancer,timeDysList,timeCanList" << endl;
        fout1 << be_onset << "," << death_age << "," << timeDysplasia << "," << timeCancer << "," << 10000 << "," << 10000 << endl;
	for(std::size_t i = 0;i < max(hgds.size(),hgc.size());i++){
		if(hgds.size()>i){
			if(hgds[i]<10000){
				fout1 << "," << "," << "," << "," << hgds[i]<< ",";
			}
		}
		if(hgc.size()>i){
			if(hgc[i]<10000){
				fout1 << hgc[i];
			}
		}
		fout1 << endl;
	}
	fout1.close();
}
//================================================================//
void InitModel(void)
{
	// Set the size of the simulation grid
	Parameters::getInstance()->cell_size(grid_size);
	Parameters::getInstance()->xdim(ni);
	Parameters::getInstance()->ydim(nj);
	Parameters::getInstance()->zdim(nk);
	// Load the free parameters
	Parameters::getInstance()->load_from_file(inputData.c_str());
	// Create the simulation grid
	tissue = new CellSpace<int>(ni,nj,nk);
	int BeSize = calculate_be_length();
	//cout << "Segment has length of " << ((double)(BeSize)*grid_size/10.0) << " cm" << endl;
	//cout << "Extends over " << (((double)(BeSize)/(double)(nj))*100.0) << "\% of length" << endl;
	// Populate it with TissueVolume objects
	for (int i = 0; i < ni; i++)
	{
		for (int j = 0; j < nj; j++)
		{
			for (int k = 0; k < nk; k++)
			{
				// Top layer has BE
				if (k == 0 && j < BeSize)
					tissue->add(new TissueVolume(BE,i,j,k),i,j,k);
				// Everything else is initially normal
				else
					tissue->add(new TissueVolume(NORMAL,i,j,k),i,j,k);
			}
		}
	}
	// Get the BE onset age
	for (int i = 0; i < 65;i++){
		if (Parameters::getInstance()->uniform()<=am_be_target[5][i]){
			be_onset = 20+i+Parameters::getInstance()->uniform();// Uniform day of the year
			break;
		}
	}
	//double mean_onset = Parameters::getInstance()->be_onset_age();
	//be_onset = 20+Parameters::getInstance()->exponential(mean_onset);//Minimum onset age is 20
	// Get the death age
	for (int i = 0; i < 101;i++){
		if (Parameters::getInstance()->uniform()<=am_life_table_arr[0][i]){
			death_age = i+Parameters::getInstance()->uniform();// Uniform day of the year
			break;
		}
	}
	// Sort the biopsies by age
	biopsy.sort();
	// Create the simulator for our tissue model
	sim = new Simulator<CellEvent<int> >(tissue);
}

int main(int argc, char **argv)
{
	unsigned ranseed = 0;
	// Read and apply the command line arguments
	for( int i = 1; i < argc; ++i )
	{
		if(strcmp( argv[i],"-var") == 0 && ++i < argc)
		{
			inputData = argv[i];
		}
		else if( strcmp( argv[i], "-ranseed" ) == 0 && ++i < argc )
		{
			ranseed = (unsigned)atol( argv[i] );
			Parameters::getInstance()->set_seed(ranseed);
		}
		else
		{
			errno = 0;
			double age = strtod(argv[i],NULL);
			if (age <= 0.0 || errno != 0)
			{
				cout << "Illegal biopsy age " << argv[i] << endl;
				return 0;
			}
			biopsy.push_back(age);
		}
	}
	// Setup the model
	InitModel();
	// Run the simulation
	int seq_num = 0;
	while (!biopsy.empty())
	{
		// Take a biopsy if next event time passes next biopsy age
		if (sim->nextEventTime()+be_onset > biopsy.front())
		{
			PrintCSV(seq_num++,ranseed,biopsy.front());
			biopsy.pop_front();
		}
		// When death occurs, kill the simulation run
		else if (sim->nextEventTime()+be_onset<death_age)
		{
			sim->execNextEvent();
		}
		else
		{
			biopsy.pop_front();
		}
	}
	// Print intervals for everyone
	vector<double> hgds;
	vector<double> hgc;
	for (int i = 0; i < ni; i++)
		for (int j = 0; j < nj; j++)
			for (int k = 0; k < nk; k++){
							double timeD = double(dynamic_cast<TissueVolume*>(tissue->getModel(i,j,k))->timeDys);
							double timeC = double(dynamic_cast<TissueVolume*>(tissue->getModel(i,j,k))->timeCan);
							if (timeD<10000){
								hgds.push_back(timeD);
								if (timeD < timeDysplasia){
									timeDysplasia=timeD;
								}
							}
							if (timeC<10000){
								hgc.push_back(timeC);
								timeCancer=timeC;
							}
						}
	PrintInterval(0,ranseed,hgds,hgc);
	// Cleanup
	delete sim;
	delete tissue;
	Parameters::deleteInstance();
	return 0;
}
