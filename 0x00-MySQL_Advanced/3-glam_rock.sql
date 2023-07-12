-- Main style for bands
SELECT band_name, 
       (YEAR('2022') - formed) AS lifespan
FROM metal_bands
WHERE main_style = 'Glam rock'
ORDER BY lifespan DESC;

