

#include <cyantities/boost.hpp>
#include <boost/units/systems/si.hpp>

#include <iostream>
#include <boost/units/io.hpp>
#include <boost/units/conversion.hpp>


/*
 *
 * From boost docs example:
 *
 */

using boost::units::length_dimension;
using boost::units::quantity;
using boost::units::unit;


namespace imperial {

struct length_base_unit :
    boost::units::base_unit<length_base_unit, length_dimension, 2>
{
    static std::string name()       { return "foot"; }
    static std::string symbol()     { return "ft"; }
};

typedef boost::units::make_system<length_base_unit>::type system;

/// unit typedefs
typedef unit<length_dimension,system>    length;

static const length foot,feet;

} // imperial

// helper for conversions between imperial length and si length
BOOST_UNITS_DEFINE_CONVERSION_FACTOR(imperial::length_base_unit,
                                     boost::units::si::meter_base_unit,
                                     double, 1.0/3.28083989501312);


/*
 *
 * End of boost docs example
 *
 */



using namespace cyantities;

namespace si = boost::units::si;


static const char* unit_name(base_unit_t i)
{
    switch (i){
        case SI_SECOND:
            return "SECOND";
        case SI_METER:
            return "METER";
        case SI_KILOGRAM:
            return "KILOGRAM";
        case SI_AMPERE:
            return "AMPERE";
        case SI_KELVIN:
            return "KELVIN";
        case SI_MOLE:
            return "MOLE";
        case SI_CANDELA:
            return "CANDELA";
        case OTHER_RADIANS:
            return "RADIAN";
    }
    return "ERROR";
}


int main(){
    /* Some static unit testing: */
//    typedef bu::divide_typeof_helper<
//        si::power,
//        si::area
//    >::type the_unit;

    typedef si::power the_unit;

    typedef bu::quantity<the_unit, double> the_quantity;

    base_unit_array_t array = get_base_unit_array<the_quantity>();

    std::cout << "the_unit base unit array:\n";
    for (size_t i=0; i<BASE_UNIT_COUNT; ++i){
        std::cout << "   " << unit_name(static_cast<base_unit_t>(i))
                  << ": " << (int)array[i] << "\n";
    }
    std::cout << "\n" << std::flush;

    std::cout << "\n\n";


    /* Now check the unit conversion: */
    UnitBuilder ub;
    ub.add_base_unit_occurrence(SI_KILOGRAM, 1);
    ub.add_base_unit_occurrence(SI_METER, 2);
    ub.add_base_unit_occurrence(SI_SECOND, -3);
    Unit unit0(ub);

    std::cout << "unit0 base unit array:\n";
    for (size_t i=0; i<BASE_UNIT_COUNT; ++i){
        std::cout << "   " << unit_name(static_cast<base_unit_t>(i))
                  << ": " << (int)array[i] << "\n";
    }
    std::cout << "\n" << std::flush;

    the_quantity P = get_converter<the_quantity>(unit0);

    std::cout << P << "\n\n\n\n" << std::flush;



    /* Conversion from metres to feet: */
    UnitBuilder ub1;
    ub1.add_base_unit_occurrence(SI_METER, 1);
    Unit unit1(ub1);
    typedef bu::quantity<imperial::length, double> feet_t;
    feet_t L = get_converter<feet_t>(unit1);

    std::cout << "1 meter in feet:\n";
    std::cout << L << "\n" << std::flush;


    return 0;
}
