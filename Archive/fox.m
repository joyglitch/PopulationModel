classdef fox < handle
    %UNTITLED3 Summary of this class goes here
    %   Detailed explanation goes here
    
    properties
        location
        step_size
        beStill = false
        age = 0;
    end
    
    methods
         function spawn(obj, rows)
             obj.location = [randi([1 rows]) randi([1 rows])];      
         end
         function step(obj)
             obj.age = obj.age + 1;
             r = rand;
             if (r > 0) && (r <= 0.125)
                 obj.location(2) = obj.location(2) + obj.step_size; % y++
             elseif (r > 0.125) && (r <= 0.250)
                 obj.location(2) = obj.location(2) + obj.step_size; % y++
                 obj.location(1) = obj.location(1) + obj.step_size; % x++
             elseif (r > 0.250) && (r <= 0.375)
                 obj.location(1) = obj.location(1) + obj.step_size; % x++
             elseif (r > 0.375) && (r <= 0.500)
                 obj.location(1) = obj.location(1) + obj.step_size; % x++
                 obj.location(2) = obj.location(2) - obj.step_size; % y--
             elseif (r > 0.500) && (r <= 0.625)
                 obj.location(2) = obj.location(2) - obj.step_size; % y--
             elseif (r > 0.625) && (r <= 0.750)
                 obj.location(2) = obj.location(2) - obj.step_size; % y--
                 obj.location(1) = obj.location(1) - obj.step_size; % x--
             elseif (r > 0.750) && (r <= 0.875)
                 obj.location(1) = obj.location(1) - obj.step_size; % x--
             else
                 obj.location(2) = obj.location(2) + obj.step_size; % y++
                 obj.location(1) = obj.location(1) - obj.step_size; % x--
             end
         end
         function locationCheck(obj, rows)
             % Check of x, if out of bounds then wrap
             if obj.location(1) > rows
                 obj.location(1) = obj.location(1) - rows;
             elseif obj.location(1) < 1
                 obj.location(1) = rows - abs(obj.location(1));
             end
             % Check of y, if out of bounds then wrap
             if obj.location(2) > rows
                 obj.location(2) = obj.location(2) - rows;
             elseif obj.location(2) < 1
                 obj.location(2) = rows - abs(obj.location(2));
             end
         end
         
    end
    
end

