
class bond_calc:
    def __init__(self,start_year: int, end_year: int, price_of_bond: int, coupon: int, principal: int):
        self.s_year = start_year
        self.e_year = end_year
        self.p_bond = price_of_bond
        self.coup = coupon
        self.princ = principal
        # values that do not need to be reset
        self.upper_bound = 100
        self.lower_bound = 0
        self.interest_rate = (self.upper_bound + self.lower_bound)/2
        self.found = False
        # values that need to be reset 
        self.b_total = 0
        self.compound_total = self.p_bond
        self.years_list = []
        self.bar_y = [-self.p_bond]
        self.reinvested_y = []
        self.scatter_y = [self.p_bond]
        
    def years_lister(self):
        if self.e_year>self.s_year:
            for year in range(1,(self.e_year-self.s_year)+1):
                self.years_list.append(year)  
            return self.years_list
        else:
            raise ValueError("End year must be after start year")

    # Limitations:
    # 1) only caluculates yield within 0 and +100% 
    # 2) Cannot calcualte negative yields as bank would never have negative intrest rate and I am calculating the break even bank interest rate instead of YTM 
    def break_even_rate (self):
        difference = self.compound_interest_total() - self.bond_total()
        # TOLERANCE = 0.01 as unlikely I will get exact match by guessing
        if abs(difference) <= 0.01:
            self.found = True
            return self.interest_rate
        elif difference > 0.01:
        # this means the interest is too high so it becomes the new upper bound
            self.upper_bound = self.interest_rate
            self.interest_rate = (self.lower_bound + self.upper_bound)/2
            return self.interest_rate
        # else it is negative and bond total is greater so guessed interest rate is too low
        else:
            # this means the interest is too low so it becomes the new lower bound
            self.lower_bound = self.interest_rate
            self.interest_rate = (self.lower_bound + self.upper_bound)/2
            return self.interest_rate
            
    def compound_interest_total(self):
        for year in self.years_list:
            self.compound_total *= (1+(self.interest_rate/100))
            self.scatter_y.append(self.compound_total)
        return self.compound_total
    
    # for positive yields coupons are assumed to be reinvested and they accumulate compund interest until maturity and that in the last year only the principal is paid without coupon
    def bond_total(self):
        for year in self.years_list:
            if not(self.s_year + year == self.e_year):
                self.b_total += (self.coup*((1+(self.interest_rate/100))**(len(self.years_list)-year)))
                self.bar_y.append(self.coup)
                self.reinvested_y.append((self.coup*(1+(self.interest_rate/100))**(len(self.years_list)-year)))
            # in the last year we simply add the principal
            elif self.s_year + year == self.e_year:
                self.b_total += self.princ
                self.bar_y.append(self.princ)
        return self.b_total
    
    def Yield(self)->float:
        i = 0
        # the loop runs up to 100 just to make sure it does not run indefinitely
        while (not(self.found)) and i<100:
            # values are reset on each iteration
            self.b_total = 0
            self.compound_total = self.p_bond
            self.bar_y = [-self.p_bond]
            self.scatter_y = [self.p_bond]
            self.years_list = []
            self.reinvested_y = []
            self.years_lister()
            i += 1
            self.break_even_rate()
        if self.found:
            return round(self.interest_rate, 2)
        else: 
            # this signifies no yield has been found
            return -1
            
        
    

