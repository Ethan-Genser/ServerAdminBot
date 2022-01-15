:: Ethan Genser 1/27/2021

for /f "tokens=2 delims==" %%a in ('wmic OS Get localdatetime /value') do set "dt=%%a"
set "YY=%dt:~2,2%" & set "YYYY=%dt:~0,4%" & set "MM=%dt:~4,2%" & set "DD=%dt:~6,2%"
set "HH=%dt:~8,2%" & set "Min=%dt:~10,2%" & set "Sec=%dt:~12,2%"

set "datestamp=%MM%-%DD%-%YYYY%" & set "timestamp=%HH%:%Min%:%Sec%"
set "fullstamp=%MM%-%DD%-%YYYY%_%HH%:%Min%:%Sec%"

"C:\Program Files (x86)\7-Zip\7z.exe" a -tzip "backups\backup %datestamp%" "world\"