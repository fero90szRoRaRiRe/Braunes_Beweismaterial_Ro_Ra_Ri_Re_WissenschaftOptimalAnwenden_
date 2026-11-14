 #include <stdio.h>
#include <string.h>

int main() {
    // Zähler/Positionen für alle vier Tentakel (Ro, Ra, Ri, Re)
    int counterRo = 1;
    int counterRa = 1;
    int counterRi = 1;
    int counterRe = 1;

    // Der Inhalt, nach dem gegriffen wird, und ein Status-Merker (0 = nicht gegriffen, 1 = gegriffen)
    char inhalt[] = "Psychologie";
    int gegriffenRo = 0;

    char eingabe;

    while (1) {
        // 1. Quaderstruktur mit printf zeichnen
        printf("\n+----------------------+-----------------+\n");
        printf("|   QUADER-STEUERUNG   | ZIEL-INHALT     |\n");
        printf("+----------------------+-----------------+\n");

        // Tentakel Ro zeichnen (mit Inhalt am Ende)
        printf("| Ro: ");
        for (int i = 0; i < 15; i++) {
            if (i < counterRo) printf("=");
            else if (i == counterRo) {
                // Wenn gegriffen wurde, ändert sich die Spitze von '>' zu 'C' (Greifer)
                if (gegriffenRo == 1) printf("C");
                else printf(">");
            }
            else printf(" ");
        }
        printf(" | %-15s |\n", inhalt); // Zeigt den Inhalt rechts neben dem Tentakel an

        // Tentakel Ra zeichnen
        printf("| Ra: ");
        for (int i = 0; i < 15; i++) {
            if (i < counterRa) printf("=");
            else if (i == counterRa) printf(">");
            else printf(" ");
        }
        printf(" |                 |\n");

        // Tentakel Ri zeichnen
        printf("| Ri: ");
        for (int i = 0; i < 15; i++) {
            if (i < counterRi) printf("=");
            else if (i == counterRi) printf(">");
            else printf(" ");
        }
        printf(" |                 |\n");

        // Tentakel Re zeichnen
        printf("| Re: ");
        for (int i = 0; i < 15; i++) {
            if (i < counterRe) printf("=");
            else if (i == counterRe) printf(">");
            else printf(" ");
        }
        printf(" |                 |\n");

        printf("+----------------------+-----------------+\n");

        // Statusmeldung, falls der Inhalt gegriffen wurde
        if (gegriffenRo == 1) {
            printf(">>> STATUS: Tentakel Ro hat den Inhalt '%s' gegriffen! <<<\n", inhalt);
        }

        // 2. Eingabe entgegennehmen
        printf("Tentakel bewegen (o = Ro, a = Ra, i = Ri, e = Re) oder 'g' zum Greifen (q = Ende): ");
        scanf(" %c", &eingabe);

        // 3. Eingabe verarbeiten
        if (eingabe == 'o') {
            if (counterRo < 14) {
                counterRo++;
            }
        } 
        else if (eingabe == 'a') {
            if (counterRa < 14) counterRa++;
        } 
        else if (eingabe == 'i') {
            if (counterRi < 14) counterRi++;
        } 
        else if (eingabe == 'e') {
            if (counterRe < 14) counterRe++;
        }
        else if (eingabe == 'g') {
            // Prüfen, ob Tentakel Ro weit genug ausgefahren ist (Position 14 = direkt am Inhalt)
            if (counterRo == 14) {
                gegriffenRo = 1;
            } else {
                printf("Tentakel Ro ist noch zu kurz zum Greifen! (Aktuell: %d/14)\n", counterRo);
            }
        }
        else if (eingabe == 'q') {
            printf("Steuerung beendet.\n");
            break;
        } 
        else {
            printf("Ungueltige Eingabe!\n");
        }
    }

    return 0;
}


