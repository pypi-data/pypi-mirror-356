# ISCC SUBTYPE WIDE

## General

The ISCC SubType WIDE shall be a SubType of the MainType ISCC that allows composite ISCC-CODEs with extended
precision for Data-Code and Instance-Code components using 128-bit digests instead of the standard 64-bit
digests.

## Purpose

The ISCC WIDE SubType shall provide enhanced precision and security for applications requiring higher confidence
in media format agnostic data identification, verification, and similarity matching, particularly in contexts
where:

1. large-scale deduplication across extensive data collections is required;
2. higher collision resistance is necessary for data integrity verification;
3. applications demand more granular distinction between similar digital assets.

## Format

An ISCC-CODE with SubType WIDE shall consist of:

1. An ISCC-HEADER with MainType ISCC and SubType WIDE;
2. An ISCC-BODY containing exactly two components:
    - A 128-bit Data-Code digest
    - A 128-bit Instance-Code digest

The total length of the ISCC-BODY for SubType WIDE shall be 256 bits (32 bytes).

!!! example "EXAMPLE: 256-bit ISCC-CODE with SubType WIDE:"

    ISCC:K4AP4P75GGHDLMRHGG2KJQY7NZEPU27HZYSYQ7HWCMHG2RRBK7E5O6Y

## SubType Assignment

The SubType WIDE shall be assigned the value 7 (0111 in binary) within the ST_ISCC enumeration for MainType
ISCC.

## Constraints

1. An ISCC-CODE with SubType WIDE shall contain only Data-Code and Instance-Code components.
2. Both the Data-Code and Instance-Code inputs shall have a length of 128 bits.
3. No other ISCC-UNIT types (META, SEMANTIC, or CONTENT) shall be included in a WIDE composite.

## Inputs

The inputs for generating an ISCC-CODE with SubType WIDE shall be:

1. A Data-Code with a minimum length of 128 bits;
2. An Instance-Code with a minimum length of 128 bits;
3. An explicit parameter indicating the intent to create a WIDE composite.

## Outputs

Processing of an ISCC-CODE with SubType WIDE shall generate the following output elements:

1. `iscc`: the ISCC-CODE in its canonical form with SubType WIDE (required);
2. `units`: an array containing the decomposed 256-bit components (optional);
3. `wide`: a boolean indicator set to true (optional);
4. any other elements collected during processing of the individual components (optional).

## Processing

### Generation

An ISCC processor shall generate an ISCC-CODE with SubType WIDE as follows:

1. Verify that exactly two ISCC-UNITs are provided: one Data-Code and one Instance-Code.
2. Verify that both input codes have a minimum length of 128 bits.
3. Verify that the explicit WIDE parameter is set to true.
4. Decode both ISCC-UNITs to binary and remove their headers.
5. Truncate the Data-Code to exactly 128 bits (16 bytes).
6. Truncate the Instance-Code to exactly 128 bits (16 bytes).
7. Concatenate the truncated Data-Code and Instance-Code to form the 256-bit ISCC-BODY.
8. Construct the ISCC-HEADER with:
    - MainType: ISCC
    - SubType: WIDE (value 7)
    - Version: 0
    - Length: encoded to represent 256 bits
9. Prefix the ISCC-BODY with the ISCC-HEADER and encode to canonical form.

### Decomposition

An ISCC processor shall decompose an ISCC-CODE with SubType WIDE as follows:

1. Decode the ISCC-CODE and extract the header.
2. Verify that the MainType is ISCC and SubType is WIDE.
3. Verify that the body length is exactly 256 bits.
4. Extract the first 128 bits as the Data-Code digest.
5. Extract the second 128 bits as the Instance-Code digest.
6. Reconstruct the individual Data-Code and Instance-Code with appropriate headers.

## Comparing

Similarity comparison for ISCC-CODEs with SubType WIDE shall follow these principles:

1. Instance-Code comparison: Two WIDE codes with identical Instance-Code components indicate the same digital
    manifestation.
2. Data-Code comparison: Calculate the binary hamming distance between the 128-bit Data-Code components. Lower
    hamming distance values indicate higher data similarity.
3. The extended 128-bit length provides approximately twice the precision of standard 64-bit comparisons,
    allowing for more granular similarity thresholds.

## Use Cases

The ISCC WIDE SubType is particularly suitable for:

1. **Digital asset management systems** requiring high-precision deduplication across millions of files;
2. **Blockchain and distributed ledger applications** where collision resistance is paramount;
3. **Content verification systems** needing enhanced confidence in data integrity;
4. **Large-scale media archives** requiring fine-grained data similarity detection.

!!! note "NOTE"

    The WIDE SubType trades increased identifier length for enhanced precision and collision resistance.
    Applications should evaluate whether the additional precision justifies the increased storage and transmission
    requirements.
