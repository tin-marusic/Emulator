clear all;
% /*
% 	parameter integer matrix [0:24]={	0, 
% 										3, 153, 8, 46, 3, 25, 1,
% 										2, 14, 4, 13, 6,
% 										0,
% 										5, 1, 1, 2, 3, 3, 4, 4, 5, 5, 6
% 										};
%                                         */
                                        
numOutputs = 720;
maxInPerOut =16; %maxInPerOut =16;
numInputs = 256;

brUlazaPoIzlazu = zeros(1, numOutputs);
brIzlazaSaMaxUlaza = 0;
matrica = zeros(numOutputs, maxInPerOut*2+1);
preostaloOsmina = ones(1, numInputs)*8;
ukupnoElemenata = numOutputs;

for i=1:brIzlazaSaMaxUlaza
    brDodanihUlaza = 0;
    dodaniUlazi = [];
    while(brDodanihUlaza<maxInPerOut)
        izabraniUlaz = randi(numInputs);
        while(ismember(izabraniUlaz, dodaniUlazi) || preostaloOsmina(izabraniUlaz)==0)
            izabraniUlaz = randi(numInputs);
        end
        dodaniUlazi = [dodaniUlazi, izabraniUlaz];
        brOsmina = randi(preostaloOsmina(izabraniUlaz));
        preostaloOsmina(izabraniUlaz)=preostaloOsmina(izabraniUlaz)-brOsmina;
        
        indeksZaUlaz = matrica(i, 1)*2+2;
        indeksZaOsminu = matrica(i, 1)*2+3;
        matrica(i, 1) = matrica(i, 1)+1;
        matrica(i, indeksZaUlaz) = izabraniUlaz-1;
        matrica(i, indeksZaOsminu) = brOsmina;
        ukupnoElemenata = ukupnoElemenata+2;
        brDodanihUlaza = brDodanihUlaza+1;
    end
end

for i=1:numInputs
    j=0;

    dodanNaIzlaze = [];
    while(preostaloOsmina(i)>0)
        brOsmina = randi(preostaloOsmina(i));
        izabraniIzlaz = randi(numOutputs-brIzlazaSaMaxUlaza)+brIzlazaSaMaxUlaza;
        % ako se ovaj ulaz vec zbraja na taj izabrani izlaz, onda izaberi drugi izlaz za ove sad osmine
        while(ismember(izabraniIzlaz, dodanNaIzlaze) || matrica(izabraniIzlaz, 1) == maxInPerOut)
            izabraniIzlaz = randi(numOutputs-brIzlazaSaMaxUlaza)+brIzlazaSaMaxUlaza;
        end
        dodanNaIzlaze = [dodanNaIzlaze, izabraniIzlaz];
        preostaloOsmina(i)=preostaloOsmina(i)-brOsmina;
        
        indeksZaUlaz = matrica(izabraniIzlaz, 1)*2+2;
        indeksZaOsminu = matrica(izabraniIzlaz, 1)*2+3;
        matrica(izabraniIzlaz, 1) = matrica(izabraniIzlaz, 1)+1;
        matrica(izabraniIzlaz, indeksZaUlaz) = i-1;
        matrica(izabraniIzlaz, indeksZaOsminu) = brOsmina;
        ukupnoElemenata = ukupnoElemenata+2;
    end
    
end


fprintf(1, '\n\n\n\n\n\n');
fprintf(1, 'parameter integer matrix [0:%d] = {\n', ukupnoElemenata-1);
for i=1:numOutputs
   if i<11
       fprintf(1, '/* output 00%d: */   ', i-1);
   elseif i>=10 && i<101
       fprintf(1, '/* output 0%d: */   ', i-1); 
   else
       fprintf(1, '/* output %d: */   ', i-1);
   end
   
   if(matrica(i, 1)==0)
       fprintf(1, '0, \n');
   else
       fprintf(1, '%d, ', matrica(i, 1));
       for j=1:matrica(i, 1)
            fprintf(1, '%d, %d, ', matrica(i, j*2), matrica(i, j*2+1));          
       end
        fprintf(1, '\n');
   end
end

fprintf(1, '};\n\n');
%matrica
fprintf(1, '\n\n\n\n\n\n');



