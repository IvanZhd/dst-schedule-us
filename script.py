# %% -------------------------------------------------------
import pandas
from datetime import datetime


class dstUS:
    ''' Define DST class for US/Canada timezone '''

    def __init__(self, startyear, endyear):
        self.years = range(startyear, endyear)
        self.schedule = pandas.DataFrame()
        self.melt = pandas.DataFrame()

    def getMonthDaysNumber(self, year, month):
        return (datetime(year, month+1, 1) - datetime(year, month, 1)).days

    def getNthSundayOfMonth(self, year, month, nthSunday):
        # List of days from 1st to 31st of March
        days = list(range(1, self.getMonthDaysNumber(year, month)+1))
        # List of days of week corresponding to date
        weekdays = list(
            map(lambda x: datetime(year, month, x).weekday(), days))
        # Get indexes of 2nd Sunday (6)
        nthSundayIdx = [i for i, d in enumerate(
            weekdays) if d == 6][nthSunday-1]
        # Get day of 2nd Sunday
        nthSundayDay = days[nthSundayIdx]
        # Get date of 2nd Sunday at 02:00:00
        nthSundayDate = datetime(year, month, nthSundayDay, 2)
        # Return formatted value
        return nthSundayDate.strftime('%Y-%m-%d %H:%M:%S')

    def getSchedule(self):
        self.schedule["secondSundaysOfMarch"] = list(
            map(lambda x: self.getNthSundayOfMonth(x, 3, 2), self.years))
        self.schedule["firstSundaysOfNovember"] = list(
            map(lambda x: self.getNthSundayOfMonth(x, 11, 1), self.years))
        self.melt = self.schedule.reset_index().melt(
            id_vars="index", value_vars=["secondSundaysOfMarch", "firstSundaysOfNovember"]).sort_values("value")


# Initialize class
dst = dstUS(2019, 2041)
# Calcualte schedule
dst.getSchedule()
# Save to file
dst.schedule.to_csv(r"./dst-schedule.csv")
dst.melt.to_csv(r"./dst-schedule-melt.csv")
# Print message
print("Done")


# %%
