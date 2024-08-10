BEGIN;
CREATETABLEalembic_version(
version_numVARCHAR(32)NOTNULLCONSTRAINTalembic_version_pkcPRIMARYKEY(
    version_num
)
);
-- Running upgrade  -> 82dd2ebb4625
CREATETABLEreformify.profile_sections(
idUUIDNOTNULL,
titleVARCHAR(256)PRIMARYKEY(
id
)
);
CREATEUNIQUEINDEX ix_reformify_profile_sections_id
ON reformify.profile_sections(
id
);
CREATETABLEreformify.user_profiles(
idVARCHARNOTNULL,
emailVARCHARNOTNULL,
passwordVARCHARNOTNULL,
fullnameVARCHAR(100)NOTNULLPRIMARYKEY(
id
)
);
CREATEUNIQUEINDEX ix_reformify_user_profiles_email
ON reformify.user_profiles(
email
);
CREATEUNIQUEINDEX ix_reformify_user_profiles_id
ON reformify.user_profiles(
id
);
CREATETABLEreformify.users(
idVARCHARNOTNULL,
emailVARCHARNOTNULL,
fullnameVARCHARNOTNULL,
passwordVARCHARNOTNULL,
deletedBOOLEANNOTNULLPRIMARYKEY(
id
),
UNIQUE(
id
)
);
CREATEUNIQUEINDEX ix_reformify_users_email
ON reformify.users(
email
);
CREATETABLEreformify.user_careers(
idVARCHARNOTNULL,
titleVARCHAR(200)NOTNULL,
start_dateVARCHARNOTNULL,
end_dateVARCHAR,
user_idVARCHARNOTNULLPRIMARYKEY(
id
),
FOREIGNKEY(user_id)REFERENCESreformify.user_profiles(
id
)
);
CREATEUNIQUEINDEX ix_reformify_user_careers_id
ON reformify.user_careers(
id
);
INSERT INTO alembic_version(
version_num
)
VALUES(
'82dd2ebb4625'
) RETURNINGalembic_version.version_num;
-- Running upgrade 82dd2ebb4625 -> 5f147b67fe3a
CREATETABLEreformify.profile_sections(
idUUIDNOTNULL,
titleVARCHAR(256)PRIMARYKEY(
id
)
);
CREATEUNIQUEINDEX ix_reformify_profile_sections_id
ON reformify.profile_sections(
id
);
CREATETABLEreformify.user_profiles(
idUUIDNOTNULL,
emailVARCHARNOTNULL,
passwordVARCHARNOTNULL,
fullnameVARCHAR(100)NOTNULL,
created_atTIMESTAMPWITHOUTTIMEZONENOTNULL,
updated_atTIMESTAMPWITHOUTTIMEZONENOTNULLPRIMARYKEY(
id
)
);
CREATEUNIQUEINDEX ix_reformify_user_profiles_email
ON reformify.user_profiles(
email
);
CREATEUNIQUEINDEX ix_reformify_user_profiles_id
ON reformify.user_profiles(
id
);
CREATETABLEreformify.users(
idVARCHARNOTNULL,
emailVARCHARNOTNULL,
fullnameVARCHARNOTNULL,
passwordVARCHARNOTNULL,
deletedBOOLEANNOTNULLPRIMARYKEY(
id
),
UNIQUE(
id
)
);
CREATEUNIQUEINDEX ix_reformify_users_email
ON reformify.users(
email
);
CREATETABLEreformify.user_careers(
idUUIDNOTNULL,
titleVARCHAR(200)NOTNULL,
start_dateVARCHARNOTNULL,
end_dateVARCHAR,
user_idUUIDNOTNULL,
created_atTIMESTAMPWITHOUTTIMEZONENOTNULL,
updated_atTIMESTAMPWITHOUTTIMEZONENOTNULLPRIMARYKEY(
id
),
FOREIGNKEY(user_id)REFERENCESreformify.user_profiles(
id
)
);
CREATEUNIQUEINDEX ix_reformify_user_careers_id
ON reformify.user_careers(
id
);
UPDATEalembic_version
SETversion_num = '5f147b67fe3a'
WHERE
alembic_version.version_num = '82dd2ebb4625';
COMMIT;
