//
// Created by polya on 7/19/24.
//

#ifndef V_INV_12_6_MC_READ_LOAD_COMPUTE_HPP
#define V_INV_12_6_MC_READ_LOAD_COMPUTE_HPP
#include "../potentialFunction/potentialFunctionPrototype.hpp"
#include <boost/filesystem.hpp>
#include <chrono>
#include <cstdlib>
#include <cxxabi.h>
#include <fstream>
#include <initializer_list>
#include <iomanip>
#include <iostream>
#include <limits>
#include <memory>
#include <random>
#include <regex>
#include <sstream>
#include <string>
#include <typeinfo>
#include <vector>

namespace fs = boost::filesystem;



class mc_computation {
public:
    mc_computation(const std::string &cppInParamsFileName) {
        std::ifstream file(cppInParamsFileName);
        if (!file.is_open()) {
            std::cerr << "Failed to open the file." << std::endl;
            std::exit(20);
        }
        std::string line;

        int paramCounter = 0;

        while (std::getline(file, line)) {
            // Check if the line is empty
            if (line.empty()) {
                continue; // Skip empty lines
            }
            std::istringstream iss(line);

            //read T
            if (paramCounter == 0) {
                iss >> T;
                if (T <= 0) {
                    std::cerr << "T must be >0" << std::endl;
                    std::exit(1);
                }//end if
                std::cout << "T=" << T << std::endl;
                this->beta = 1 / T;
                double stepForT1 = 0.1;
                this->h = stepForT1 * T > 0.2 ? 0.2 : stepForT1 * T;//stepSize;
                std::cout << "h=" << h << std::endl;
                paramCounter++;
                continue;
            }//end reading T
            //read coefficients
            if(paramCounter==1){
                iss>>coefsToPotFunc;
                paramCounter++;
                continue;

            }// end reading coefficients


            //read potential function name
            if(paramCounter==2){
                iss>>potFuncName;
                paramCounter++;
                continue;
            }//end reading potential function name

            //read initial values
            if(paramCounter==3){
                std::string temp;
                if (std::getline(iss, temp, ',')){
                    LInit=std::stod(temp);
                }
                if (std::getline(iss, temp, ',')){
                    y0Init=std::stod(temp);
                }
                if (std::getline(iss, temp, ',')){
                    z0Init=std::stod(temp);
                }
                if (std::getline(iss, temp, ',')){
                    y1Init=std::stod(temp);
                }
                paramCounter++;
                continue;




            }//end reading initial values


            //read loopToWrite
            if(paramCounter==4){
                //if loopLastFileStr is "-1", loopLastFile uses the overflowed value
                //and loopLastFile+1 will be 0
                iss>>loopToWrite;
                paramCounter++;
                continue;
            }//end reading loopToWrite

            //read newFlushNum
            if(paramCounter==5){
                iss>>newFlushNum;
                paramCounter++;
                continue;
            }//end reading newFlushNum

            //read loopLastFile
            if(paramCounter==6){
                iss>>loopLastFile;
                paramCounter++;
                continue;
            }//end reading loopLastFile

            //read TDirRoot
            if (paramCounter==7){
                iss>>TDirRoot;
                paramCounter++;
                continue;
            }//end reading TDirRoot

            //read U_dist_dataDir
            if(paramCounter==8){
                iss>>U_dist_dataDir;
                paramCounter++;
                continue;
            }//end reading U_dist_dataDir



        }//end while
        this->potFuncPtr = createPotentialFunction(potFuncName, coefsToPotFunc);
        potFuncPtr->init();
        this->varNum = 5;
        try {
            this->U_dist_ptr= std::shared_ptr<double[]>(new double[loopToWrite * varNum],
                                                        std::default_delete<double[]>());
        }
        catch (const std::bad_alloc &e) {
            std::cerr << "Memory allocation error: " << e.what() << std::endl;
            std::exit(2);
        } catch (const std::exception &e) {
            std::cerr << "Exception: " << e.what() << std::endl;
            std::exit(2);
        }
        std::cout<<"LInit="<<LInit<<", y0Init="<<y0Init
                 <<", z0Init="<<z0Init<<", y1Init="<<y1Init<<std::endl;

        std::cout<<"loopToWrite="<<loopToWrite<<std::endl;
        std::cout<<"newFlushNum="<<newFlushNum<<std::endl;
        std::cout<<"loopLastFile+1="<<loopLastFile+1<<std::endl;
        std::cout<<"TDirRoot="<<TDirRoot<<std::endl;
        std::cout<<"U_dist_dataDir="<<U_dist_dataDir<<std::endl;

    }//end constructor




public:
    ///
    /// @param x
    /// @param leftEnd
    /// @param rightEnd
    /// @param eps
    /// @return return a value within distance eps from x, on the open interval (leftEnd, rightEnd)
   double generate_uni_open_inteval(const double &x, const double &leftEnd, const double &rightEnd, const double &eps);



    ///
    /// @param LCurr current value of L
    /// @param y0Curr current value of y0
    /// @param z0Curr current value of z0
    /// @param y1Curr current value of y1
    /// @param LNext  next value of L
    /// @param y0Next next value of y0
    /// @param z0Next next value of z0
    /// @param y1Next next value of y1
    void proposal(const double &LCurr, const double& y0Curr,const double& z0Curr, const double& y1Curr,
                  double & LNext, double & y0Next, double & z0Next, double & y1Next);


    ///
    /// @param LCurr
    /// @param y0Curr
    /// @param z0Curr
    /// @param y1Curr
    /// @param LNext
    /// @param y0Next
    /// @param z0Next
    /// @param y1Next
    /// @param UNext
    /// @return
    double acceptanceRatio(const double &LCurr,const double &y0Curr,
                           const double &z0Curr, const double& y1Curr,const double& UCurr,
                           const double &LNext, const double& y0Next,
                           const double & z0Next, const double & y1Next,
                           double &UNext);


public:
    double T;// temperature
    double beta;
    double h;// step size
    size_t loopToWrite;
    size_t newFlushNum;
    size_t loopLastFile;
    std::shared_ptr<potentialFunction> potFuncPtr;
    std::string TDirRoot;
    std::string U_dist_dataDir;
    std::shared_ptr<double[]> U_dist_ptr;
    size_t varNum;
    double LInit;
    double y0Init;
    double z0Init;
    double y1Init;
    std::string coefsToPotFunc;
    std::string potFuncName;

};


#endif //V_INV_12_6_MC_READ_LOAD_COMPUTE_HPP
