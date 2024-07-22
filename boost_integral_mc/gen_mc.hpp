//
// Created by polya on 7/22/24.
//

#ifndef V_INV_12_6_GEN_MC_HPP
#define V_INV_12_6_GEN_MC_HPP
#include <boost/filesystem.hpp>
#include <boost/math/quadrature/trapezoidal.hpp>
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
const auto PI=M_PI;

class gen_data{

public:gen_data() {

        this->a = 1.0;
        this->b = 2.0;
        this->sgm = 0.1;
        this->xInit=a+(b-a)/1.76;

        this->M = std::pow(2.0 * PI, 0.5) * sgm * 1.001;
        dataDir = "./boost_int_mc/";
        if (!fs::is_directory(dataDir) || !fs::exists(dataDir)) {
            fs::create_directories(dataDir);
        }
        loopToWrite = 1000000;
        newFlushNum = 5;

        this->dataAll = std::shared_ptr<double[]>(new double[loopToWrite],
                                                  std::default_delete<double[]>());

    }

public:
///proportional to probability, target mc distribution
double g(const double &x);


///
/// @param y
/// @param x center
/// @return known proposal function, which is normal distribution
double Q(const double &y, const double &x);


///
/// @param x center
/// @return random number from truncated Gaussian
double reject_sampling_one_data(const double &x);

///
/// @param y
/// @param x center
/// @return truncated Gaussian
double f(const double &y, const double& x);

///
/// @param xCurr
/// @param xNext
/// @return
void proposal(const double &xCurr, double &xNext);

///
/// @param x center
/// @return integral
double zVal(const double& x);

///
/// @param xCurr
/// @param xNext
/// @return
double  acceptanceRatio(const double &xCurr, const double &xNext);


///
/// @param y
/// @param x center
/// @return
double integrand(const double &y, const double& x);

void execute_mc(const double& x);


void saveArrayToCSV(const std::shared_ptr<double[]>& array, const  size_t& arraySize, const std::string& filename);

    void init_and_run();

public:
    double a;
    double b;
    double sgm;
    double xInit;

    double M;
    std::string dataDir;
    std::shared_ptr<double[]> dataAll;
    size_t loopToWrite;
    size_t newFlushNum;

};


#endif //V_INV_12_6_GEN_MC_HPP
