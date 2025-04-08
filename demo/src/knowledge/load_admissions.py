"""
Script to load Concordia University admission information into the vector database.
"""

import os
import sys
import asyncio

# Add the project root to the Python path
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(project_root)

from demo.src.knowledge.vector_store import VectorStore

# Admission information
admission_texts = [
    # Section 1: Undergraduate Application for the Bachelor of Computer Science (BCompSc)
    "1. The Bachelor of Computer Science program is offered by the Department of Computer Science and Software Engineering at the Gina Cody School of Engineering and Computer Science; it lasts 3 to 4 years and includes experiential co-op work terms.",
    "2. The admissions page features a prominent 'APPLY NOW' call-to-action for prospective students.",
    "3. For Quebec CEGEP applicants, an overall average of 27 (or 26 in math) is required along with completion of key DEC courses including Calculus 1, Calculus 2, and Linear Algebra.",
    "4. High school applicants must achieve an overall grade of A–, with A– in math as a strong requirement, or demonstrate equivalent high academic standing.",
    "5. International high school applicants should note that ACT/SAT scores are not required and AP exams are not mandatory but may qualify for advanced standing.",
    "6. Special funding of up to $4,000 is available for out-of-province undergraduate students.",
    "7. For Fall Entry, domestic applicants must submit applications by March 1, while international applicants are advised to apply by February 1 to allow for immigration processing.",
    "8. For Winter Entry, domestic applicants must apply by November 1, and international applicants should submit by August 1.",

    # Section 2: Curriculum and Academic Policy Updates
    "9. Curriculum updates (as per the November 26, 2020 letter) note modifications in course sequences and prerequisites for the Bachelor of Computer Science.",
    "10. All required 200-level courses must be completed with a minimum grade of C– or better before students can register for 400-level courses.",
    "11. Should a student receive a grade of D+ or lower in any required 200-level course, it must be repeated before taking any dependent courses.",
    "12. Graduation does not occur automatically; students must formally apply for graduation following the provided instructions.",

    # Section 3: General (Often Graduate) Application Process – Steps 1 to 4
    "13. Step 1: Applicants must select the program that best aligns with their academic and career goals.",
    "14. For graduate studies, prospective applicants should review the detailed program pages and contact the Graduate Program Director with any questions.",
    "15. Step 2: For doctoral programs, applicants must have completed a master's (or equivalent) with high standing, or present an outstanding bachelor's record to be eligible for direct-entry to a PhD.",
    "16. Applicants for master's, diploma, or graduate certificate programs must hold a bachelor's degree with high standing (typically equivalent to a B average or higher).",
    "17. Unofficial transcripts are to be uploaded initially to speed up the review process, with official transcripts required once admitted.",
    "18. Most applications require three letters of reference from individuals who can attest to the applicant's academic potential.",
    "19. A Statement of Purpose—usually about 600 words—must detail the applicant's academic and professional experience and explain why Concordia is the right fit.",
    "20. Additional supporting documents such as language test scores (e.g., TOEFL or IELTS), a curriculum vitae (CV), and any legal documents are also required.",
    "21. Mailing and courier instructions are provided for official transcripts if the applicant is studying outside Canada or the United States.",
    "22. Step 3: Applicants must create their Concordia account (Netname) to begin and manage their application.",
    "23. It is important to have digital copies (PDFs) of transcripts, letters of reference, and all other documents ready prior to starting the application.",
    "24. Applicants must have a valid credit or debit card available to pay the non-refundable application fee (e.g., $100 CAD for most graduate applications).",
    "25. Online application instructions should be followed carefully; avoid using the browser's back button and remember to click 'Save and Exit' when necessary.",
    "26. Step 4: Once the application is submitted, a confirmation email—typically arriving within 24 hours and including an eight-digit student ID—will be sent.",
    "27. Applicants are advised to check their Student Centre regularly for application status updates and any additional document requests.",
    "28. It is essential to follow up with referees if their letters of reference are not submitted in a timely manner.",

    # Section 4: International High School Requirements
    "29. International high school applicants must graduate from an accredited high school; for American curriculum schools, a school profile should be submitted.",
    "30. ACT and SAT scores are not required for international high school applicants.",
    "31. AP exams are optional for international high school applicants, though strong scores may grant advanced standing.",
    "32. Applicants should also review Canadian provincial curriculum course requirements as detailed in the A-Z program list.",

    # Section 5: Baccalauréat français Details
    "33. Baccalauréat français applicants are admitted to the 120-credit Extended Credit Program (ECP).",
    "34. Transfer credits are awarded for Spécialité courses if a minimum score of 12 is achieved.",
    "35. Applicants can receive up to 12 transfer credits per Spécialité course completed in Terminale, with a maximum of 24 transfer credits overall.",
    "36. The baccalauréat professionnel is not accepted for admission.",
    "37. Applicants completing the Baccalauréat français in Quebec must also submit the results from the compléments d'enseignement québécois.",
    "38. For BA and BEd programs under Baccalauréat français, there are generally no specific subject prerequisites.",
    "39. For BA – all Mathematics programs, it is recommended that students complete Première in Spécialité mathématiques.",
    "40. For the Bachelor of Computer Science (BCompSc), both Première and Terminale in Spécialité mathématiques are required.",
    "41. For BCompSc – Health and Life Sciences, applicants must complete courses in Spécialité mathématiques and Spécialité physique-chimie at both Première and Terminale levels.",
    "42. The Certificate in Science and Technology requires the completion of Première: Spécialité mathématiques.",
    "43. For the John Molson School of Business BComm program, a background in Première: Spécialité mathématiques is required, with Terminale results in Mathématiques complémentaires or Spécialité mathématiques.",
    "44. For Certificate in Business Studies and Certificate Foundations for Business, subject prerequisites are focused on mathematics.",

    # Section 6: International Baccalaureate (IB) Diploma Programme Details
    "45. IB Diploma Programme applicants are admitted to the 120-credit Extended Credit Program (ECP).",
    "46. Transfer credits are awarded for Higher Level (HL) courses when a minimum score of 4 is achieved.",
    "47. Students may receive up to 9 transfer credits per HL course for a maximum of 27 transfer credits.",
    "48. Accepted math courses include Mathematics: Applications and Interpretations HL, as well as Mathematics: Analysis and Approaches (SL or HL).",
    "49. BA programs under the IB do not always require specific subject prerequisites.",
    "50. For BA – all Mathematics programs, a focused math requirement is enforced under IB standards.",
    "51. The BComm program requires a math component when applicants enter via the IB route.",
    "52. The Bachelor of Computer Science (BCompSc) requires a strong math background under IB admissions.",
    "53. For BCompSc – Health and Life Sciences, both math and one science (Biology, Chemistry, or Physics) are required under the IB system.",
    "54. BEd programs under IB generally do not have specific subject prerequisites.",
    "55. For BSc programs, a combination of math and one science is required when applying via the IB Diploma.",
    "56. In BEng programs, applicants must have completed math and Physics—with at least one taken at the Higher Level.",
    "57. BFA programs typically have no specific subject prerequisites under IB criteria.",
    "58. For BFA – Computation Arts with Computer Science, a math component is required in the IB admissions process.",

    # Section 7: International Baccalaureate Career-related Programme (IB CP)
    "59. IB CP applicants are also admitted to the 120-credit Extended Credit Program (ECP).",
    "60. All IB CP candidates must have a minimum of 3 IB subjects, with at least 2 at the Higher Level.",
    "61. Transfer credits and exemptions for IB CP candidates are assessed on a case-by-case basis.",
    "62. For BA programs under IB CP, there are generally no subject prerequisites.",
    "63. For BA – all Mathematics programs under IB CP, a math requirement is enforced.",
    "64. BComm applicants under IB CP must meet a math requirement.",
    "65. BCompSc applicants via IB CP need a strong math component.",
    "66. For BCompSc – Health and Life Sciences via IB CP, both math and one science are required.",
    "67. BEd applicants under IB CP are not required to meet specific subject prerequisites.",
    "68. BSc programs under IB CP require a combination of math and one science.",
    "69. In IB CP, BEng programs demand completion of math and Physics.",
    "70. BFA programs under IB CP generally do not have defined subject prerequisites.",
    "71. For BFA – Computation Arts with Computer Science via IB CP, a math requirement is necessary.",

    # Section 8: British System of Education (GCE) Requirements
    "72. Applicants holding A-levels are required to have completed two A-level examinations.",
    "73. In addition to A-levels, applicants may submit final grades from lower sixth form along with AS-level and iGCSE/GCSE/O-level results.",
    "74. For those with AS-level qualifications, four AS-level exams are required.",
    "75. Applicants with GCSE or equivalent qualifications must have completed one year of higher education post-GCSE.",
    "76. BTEC Level 3 or extended diplomas are accepted as equivalent to at least two A-levels.",
    "77. Students applying for programs with math or science requirements may be evaluated based on AS-level or GCSE results if A-levels are not available.",
    "78. Typical entry for BA programs via the British system is in the range of CD to CC.",
    "79. For BA – all Mathematics programs, entry generally requires results from CD up to AA with Math grades ranging from D to A.",
    "80. Admission to the BComm program typically requires a result of CC with a Math C.",
    "81. For the Bachelor of Computer Science (BCompSc), entry is generally at the level of AB with a Math B.",
    "82. BCompSc – Health and Life Sciences entry usually demands AB with Math B and Science B.",
    "83. BEd programs often require an entry level of CC.",
    "84. BEng programs typically accept applicants with grades ranging from CD to AB, with Math grades from C to B and Physics from C to A.",
    "85. Entry into BFA programs commonly requires a CD level result.",
    "86. For BFA – Computation Arts with Computer Science, applicants are generally expected to have results at the AB level with a Math B.",
    "87. BSc programs via the British system typically require results from CD up to AA with Math and Science grades ranging from D to A.",

    # Section 9: Country/Region Specific Admission Certificates (selected examples)
    "88. Afghanistan: Applicants must provide a 12th Grade Graduation Certificate.",
    "89. Albania: Applicants must present a 'Dëftesë Pjekurie' or a Diploma of State Matura.",
    "90. Algeria: Submission of the Baccalauréat de l'enseignement secondaire is required.",
    "91. Argentina: Applicants should possess either a Bachiller, Bachiller especializado, or Titulo de Bachiller.",
    "92. Armenia: A Certificate of Complete Secondary General Education or an equivalent is necessary.",
    "93. Australia: Applicants must hold a Year 12 upper secondary school certificate or a Certificate VI for Vocational Education and Training (VET).",
    "94. Austria: A Reifeprüfungszeugnis, a Vocational Education Certificate, or a comparable document is required.",
    "95. Belgium: Submission of a Diploma van Secundair Onderwijs or a Certificate of Higher Secondary Education is mandatory.",
    "96. Brazil: A Certificado de Ensino Medio or an equivalent qualification is required.",
    "97. China: Applicants must present a Senior Middle School Graduation Certificate or a General Secondary Education Certificate.",
    "98. Denmark: An Upper Secondary School Leaving Certificate (e.g., the Studentereksamen) is required.",
    "99. France: A Baccalauréat général or Baccalauréat technologique must be provided.",
    "100. Germany: A Zeugnis der Allgemeinen Hochschulreife is required.",
    "101. India: Applicants are expected to have a Higher School Certificate or an equivalent qualification.",

    # Section 10: Home-schooled Applicants
    "102. Home-schooled applicants are evaluated on a case-by-case basis.",
    "103. They must submit transcripts and any standardized test scores (e.g., SAT and/or AP scores) from any attended institution.",
    "104. A detailed description of the home-school curriculum followed is required.",
    "105. Applicants must provide a letter of intent explaining their academic background and why they are a strong candidate.",
    "106. In addition, a letter from the home-educator and a recommendation from an impartial source are required.",

    # Section 11: Advanced Placement (AP) Courses and Credits
    "107. Successful AP examinations (grade 3 or better) may qualify for up to 30 transfer credits.",
    "108. Transfer credits and course exemptions based on AP exam scores will be detailed in the admission offer.",
    "109. AP Art History scores may grant credit for courses like ARTH 201/202 or GFAR as per Concordia's guidelines.",
    "110. AP Biology scores may translate into credit for BIOL 201 and first-year biology courses.",
    "111. A passing score on AP Calculus AB may grant credit for MATH 203 and exemptions from MATH 201, 206, and 209.",
    "112. AP Calculus BC scores may provide credit for MATH 203 and MATH 205, with similar exemptions.",
    "113. AP Chemistry scores may allow for credit in CHEM 205 and CHEM 206.",
    "114. AP Computer Science A may grant credit for COMP 248.",
    "115. Other AP exam subjects in English, Economics, History, etc., have defined transfer credits according to Concordia's equivalencies.",
    "116. A minimum grade of 4 is required on AP exams in subjects marked with an asterisk for credit eligibility.",

    # Section 12: English Language Proficiency
    "117. If the applicant's primary language is not English, a proficiency test (e.g., TOEFL or IELTS) is required.",
    "118. Applicants must meet the minimum English language standards as defined by Concordia.",

    # Section 13: Immigration and Financial Information
    "119. Non-Canadian citizens or permanent residents must obtain both a Certificat d'acceptation du Québec (CAQ) and a Canadian Study Permit for programs lasting more than six months.",
    "120. Programs lasting less than six months do not require a CAQ or Study Permit.",
    "121. Applicants should begin their immigration document process immediately after receiving an Offer of Admission.",
    "122. Refugees and refugee claimants are considered international students and must obtain a CAQ/CSQ along with a Study Permit.",
    "123. Evidence of sufficient funds for tuition and living expenses must be provided during the immigration process.",
    "124. Detailed financial requirements can be found on the Tuition and Fees webpage, and inquiries about on/off campus work regulations should be directed to the International Students Office."
]

metadatas = [
    # Section 1 Metadata: Undergraduate BCompSc program overview and deadlines
    {"university": "Concordia", "program": "BCompSc", "level": "undergraduate", "type": "overview"},
    {"university": "Concordia", "program": "BCompSc", "level": "undergraduate", "type": "overview"},
    {"university": "Concordia", "program": "BCompSc", "level": "undergraduate", "type": "requirements"},
    {"university": "Concordia", "program": "BCompSc", "level": "undergraduate", "type": "requirements"},
    {"university": "Concordia", "program": "BCompSc", "level": "international", "type": "requirements"},
    {"university": "Concordia", "program": "BCompSc", "level": "undergraduate", "type": "funding"},
    {"university": "Concordia", "program": "BCompSc", "level": "undergraduate", "type": "deadline"},
    {"university": "Concordia", "program": "BCompSc", "level": "undergraduate", "type": "deadline"},

    # Section 2 Metadata: Curriculum and academic policies
    {"university": "Concordia", "program": "BCompSc", "level": "undergraduate", "type": "academic_policy"},
    {"university": "Concordia", "program": "BCompSc", "level": "undergraduate", "type": "academic_policy"},
    {"university": "Concordia", "program": "BCompSc", "level": "undergraduate", "type": "academic_policy"},
    {"university": "Concordia", "program": "BCompSc", "level": "undergraduate", "type": "academic_policy"},

    # Section 3 Metadata: General application process (Steps 1–4)
    {"university": "Concordia", "program": "General", "level": "all", "type": "process"},
    {"university": "Concordia", "program": "Graduate", "level": "graduate", "type": "process"},
    {"university": "Concordia", "program": "Doctoral", "level": "doctoral", "type": "requirements"},
    {"university": "Concordia", "program": "Graduate", "level": "graduate", "type": "requirements"},
    {"university": "Concordia", "program": "General", "level": "all", "type": "documents"},
    {"university": "Concordia", "program": "General", "level": "all", "type": "documents"},
    {"university": "Concordia", "program": "Graduate", "level": "graduate", "type": "documents"},
    {"university": "Concordia", "program": "Graduate", "level": "graduate", "type": "documents"},
    {"university": "Concordia", "program": "International", "level": "international", "type": "documents"},
    {"university": "Concordia", "program": "General", "level": "all", "type": "process"},
    {"university": "Concordia", "program": "General", "level": "all", "type": "documents"},
    {"university": "Concordia", "program": "General", "level": "all", "type": "financial"},
    {"university": "Concordia", "program": "General", "level": "all", "type": "process"},
    {"university": "Concordia", "program": "General", "level": "all", "type": "process"},
    {"university": "Concordia", "program": "General", "level": "all", "type": "process"},
    {"university": "Concordia", "program": "General", "level": "all", "type": "process"},
    {"university": "Concordia", "program": "General", "level": "all", "type": "process"},
    {"university": "Concordia", "program": "General", "level": "all", "type": "process"},
    {"university": "Concordia", "program": "General", "level": "all", "type": "process"},

    # Section 4 Metadata: International High School Requirements
    {"university": "Concordia", "program": "International", "level": "international", "type": "requirements"},
    {"university": "Concordia", "program": "International", "level": "international", "type": "requirements"},
    {"university": "Concordia", "program": "International", "level": "international", "type": "requirements"},
    {"university": "Concordia", "program": "International", "level": "international", "type": "requirements"},

    # Section 5 Metadata: Baccalauréat français Details
    {"university": "Concordia", "program": "Baccalauréat français", "level": "international", "type": "requirements"},
    {"university": "Concordia", "program": "Baccalauréat français", "level": "international", "type": "credits"},
    {"university": "Concordia", "program": "Baccalauréat français", "level": "international", "type": "credits"},
    {"university": "Concordia", "program": "Baccalauréat français", "level": "international", "type": "requirements"},
    {"university": "Concordia", "program": "Baccalauréat français", "level": "international", "type": "requirements"},
    {"university": "Concordia", "program": "Baccalauréat français", "level": "international", "type": "requirements"},
    {"university": "Concordia", "program": "BA – Mathematics", "level": "international", "type": "recommendations"},
    {"university": "Concordia", "program": "BCompSc", "level": "undergraduate", "type": "requirements"},
    {"university": "Concordia", "program": "BCompSc – Health & Life Sciences", "level": "undergraduate", "type": "requirements"},
    {"university": "Concordia", "program": "Certificate in Science and Technology", "level": "international", "type": "requirements"},
    {"university": "Concordia", "program": "BComm", "level": "international", "type": "requirements"},
    {"university": "Concordia", "program": "Business Certificates", "level": "international", "type": "requirements"},

    # Section 6 Metadata: International Baccalaureate (IB) Diploma Programme
    {"university": "Concordia", "program": "IB Diploma", "level": "international", "type": "requirements"},
    {"university": "Concordia", "program": "IB Diploma", "level": "international", "type": "credits"},
    {"university": "Concordia", "program": "IB Diploma", "level": "international", "type": "credits"},
    {"university": "Concordia", "program": "IB Diploma", "level": "international", "type": "requirements"},
    {"university": "Concordia", "program": "BA", "level": "international", "type": "requirements"},
    {"university": "Concordia", "program": "BA – Mathematics", "level": "international", "type": "requirements"},
    {"university": "Concordia", "program": "BComm", "level": "international", "type": "requirements"},
    {"university": "Concordia", "program": "BCompSc", "level": "international", "type": "requirements"},
    {"university": "Concordia", "program": "BCompSc – Health & Life Sciences", "level": "undergraduate", "type": "requirements"},
    {"university": "Concordia", "program": "BEd", "level": "international", "type": "requirements"},
    {"university": "Concordia", "program": "BSc", "level": "undergraduate", "type": "requirements"},
    {"university": "Concordia", "program": "BEng", "level": "undergraduate", "type": "requirements"},
    {"university": "Concordia", "program": "BFA", "level": "international", "type": "requirements"},
    {"university": "Concordia", "program": "BFA – Computation Arts", "level": "international", "type": "requirements"},

    # Section 7 Metadata: IB Career-related Programme (CP)
    {"university": "Concordia", "program": "IB CP", "level": "international", "type": "requirements"},
    {"university": "Concordia", "program": "IB CP", "level": "international", "type": "requirements"},
    {"university": "Concordia", "program": "IB CP", "level": "international", "type": "credits"},
    {"university": "Concordia", "program": "BA", "level": "international", "type": "requirements"},
    {"university": "Concordia", "program": "BA – Mathematics", "level": "international", "type": "requirements"},
    {"university": "Concordia", "program": "BComm", "level": "international", "type": "requirements"},
    {"university": "Concordia", "program": "BCompSc", "level": "international", "type": "requirements"},
    {"university": "Concordia", "program": "BCompSc – Health & Life Sciences", "level": "undergraduate", "type": "requirements"},
    {"university": "Concordia", "program": "BEd", "level": "international", "type": "requirements"},
    {"university": "Concordia", "program": "BSc", "level": "undergraduate", "type": "requirements"},
    {"university": "Concordia", "program": "BEng", "level": "undergraduate", "type": "requirements"},
    {"university": "Concordia", "program": "BFA", "level": "international", "type": "requirements"},
    {"university": "Concordia", "program": "BFA – Computation Arts", "level": "international", "type": "requirements"},

    # Section 8 Metadata: British System of Education (GCE)
    {"university": "Concordia", "program": "GCE", "level": "international", "type": "requirements"},
    {"university": "Concordia", "program": "GCE", "level": "international", "type": "requirements"},
    {"university": "Concordia", "program": "GCE", "level": "international", "type": "requirements"},
    {"university": "Concordia", "program": "GCE", "level": "international", "type": "requirements"},
    {"university": "Concordia", "program": "GCE", "level": "international", "type": "requirements"},
    {"university": "Concordia", "program": "GCE", "level": "international", "type": "requirements"},
    {"university": "Concordia", "program": "BA", "level": "international", "type": "requirements"},
    {"university": "Concordia", "program": "BA – Mathematics", "level": "international", "type": "requirements"},
    {"university": "Concordia", "program": "BComm", "level": "international", "type": "requirements"},
    {"university": "Concordia", "program": "BCompSc", "level": "undergraduate", "type": "requirements"},
    {"university": "Concordia", "program": "BCompSc – Health & Life Sciences", "level": "undergraduate", "type": "requirements"},
    {"university": "Concordia", "program": "BEd", "level": "international", "type": "requirements"},
    {"university": "Concordia", "program": "BEng", "level": "undergraduate", "type": "requirements"},
    {"university": "Concordia", "program": "BFA", "level": "international", "type": "requirements"},
    {"university": "Concordia", "program": "BFA – Computation Arts", "level": "international", "type": "requirements"},
    {"university": "Concordia", "program": "BSc", "level": "undergraduate", "type": "requirements"},

    # Section 9 Metadata: Country/Region Specific Requirements
    {"university": "Concordia", "program": "International", "level": "international", "type": "country_requirements"},
    {"university": "Concordia", "program": "International", "level": "international", "type": "country_requirements"},
    {"university": "Concordia", "program": "International", "level": "international", "type": "country_requirements"},
    {"university": "Concordia", "program": "International", "level": "international", "type": "country_requirements"},
    {"university": "Concordia", "program": "International", "level": "international", "type": "country_requirements"},
    {"university": "Concordia", "program": "International", "level": "international", "type": "country_requirements"},
    {"university": "Concordia", "program": "International", "level": "international", "type": "country_requirements"},
    {"university": "Concordia", "program": "International", "level": "international", "type": "country_requirements"},
    {"university": "Concordia", "program": "International", "level": "international", "type": "country_requirements"},
    {"university": "Concordia", "program": "International", "level": "international", "type": "country_requirements"},
    {"university": "Concordia", "program": "International", "level": "international", "type": "country_requirements"},
    {"university": "Concordia", "program": "International", "level": "international", "type": "country_requirements"},
    {"university": "Concordia", "program": "International", "level": "international", "type": "country_requirements"},

    # Section 10 Metadata: Home-schooled Applicants
    {"university": "Concordia", "program": "Home-schooled", "level": "international", "type": "requirements"},
    {"university": "Concordia", "program": "Home-schooled", "level": "international", "type": "documents"},
    {"university": "Concordia", "program": "Home-schooled", "level": "international", "type": "requirements"},
    {"university": "Concordia", "program": "Home-schooled", "level": "international", "type": "documents"},
    {"university": "Concordia", "program": "Home-schooled", "level": "international", "type": "documents"},

    # Section 11 Metadata: Advanced Placement (AP) Courses and Credits
    {"university": "Concordia", "program": "Advanced Placement", "level": "international", "type": "credits"},
    {"university": "Concordia", "program": "Advanced Placement", "level": "international", "type": "credits"},
    {"university": "Concordia", "program": "Advanced Placement", "level": "international", "type": "credits"},
    {"university": "Concordia", "program": "Advanced Placement", "level": "international", "type": "credits"},
    {"university": "Concordia", "program": "Advanced Placement", "level": "international", "type": "credits"},
    {"university": "Concordia", "program": "Advanced Placement", "level": "international", "type": "credits"},
    {"university": "Concordia", "program": "Advanced Placement", "level": "international", "type": "credits"},
    {"university": "Concordia", "program": "Advanced Placement", "level": "international", "type": "credits"},
    {"university": "Concordia", "program": "Advanced Placement", "level": "international", "type": "credits"},

    # Section 12 Metadata: English Language Proficiency
    {"university": "Concordia", "program": "English Proficiency", "level": "international", "type": "requirements"},
    {"university": "Concordia", "program": "English Proficiency", "level": "international", "type": "requirements"},

    # Section 13 Metadata: Immigration and Financial Information
    {"university": "Concordia", "program": "Immigration/Financial", "level": "international", "type": "immigration"},
    {"university": "Concordia", "program": "Immigration/Financial", "level": "international", "type": "immigration"},
    {"university": "Concordia", "program": "Immigration/Financial", "level": "international", "type": "immigration"},
    {"university": "Concordia", "program": "Immigration/Financial", "level": "international", "type": "immigration"},
    {"university": "Concordia", "program": "Immigration/Financial", "level": "international", "type": "financial"},
    {"university": "Concordia", "program": "Immigration/Financial", "level": "international", "type": "financial"},
    {"university": "Concordia", "program": "Immigration/Financial", "level": "international", "type": "financial"},
    {"university": "Concordia", "program": "Immigration/Financial", "level": "international", "type": "financial"}
]

async def load_admissions_data():
    """Load admission information into the vector database."""
    # Create a vector store for admissions
    admissions_store = VectorStore(collection_name="concordia_admissions")
    
    # Add the admission texts with metadata
    await admissions_store.add_texts(admission_texts, metadatas=metadatas)
    
    print(f"Successfully loaded {len(admission_texts)} admission entries into the vector database.")

if __name__ == "__main__":
    asyncio.run(load_admissions_data()) 