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

class gen_data{

public:gen_data(){

        this->a=1;
         this->b=2;
        this->sgm=0.1;
        this->M=
}

public:
///proportional to probability
double f(const double &x);

///
/// @param y
/// @param x
/// @return known proposal function
double Q(const double &y, const double &x);


public:
    double a;
    double b;
    double sgm;

    double M;

};


#endif //V_INV_12_6_GEN_MC_HPP
