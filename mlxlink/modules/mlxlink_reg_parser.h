/*
 * Copyright (c) 2019-2021 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
 *
 * This software is available to you under a choice of one of two
 * licenses.  You may choose to be licensed under the terms of the GNU
 * General Public License (GPL) Version 2, available from the file
 * COPYING in the main directory of this source tree, or the
 * OpenIB.org BSD license below:
 *
 *     Redistribution and use in source and binary forms, with or
 *     without modification, are permitted provided that the following
 *     conditions are met:
 *
 *      - Redistributions of source code must retain the above
 *        copyright notice, this list of conditions and the following
 *        disclaimer.
 *
 *      - Redistributions in binary form must reproduce the above
 *        copyright notice, this list of conditions and the following
 *        disclaimer in the documentation and/or other materials
 *        provided with the distribution.
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
 * EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
 * MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
 * NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS
 * BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN
 * ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
 * CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
 * SOFTWARE.

 *
 */
#ifndef MLXLINK_REG_PARSER_H
#define MLXLINK_REG_PARSER_H

#include "mlxlink_utils.h"
#include <mtcr.h>

using namespace mlxreg;
#define PRINT_LOG(mlxlinklogger, title)                 \
    if (mlxlinklogger)                                  \
    {                                                   \
        mlxlinklogger->printHeaderWithUnderLine(title); \
    }

#define DEBUG_LOG(mlxlinklogger, format, ...)         \
    if (mlxlinklogger)                                \
    {                                                 \
        mlxlinklogger->debugLog(format, __VA_ARGS__); \
    }

#define PDDR_STATUS_MESSAGE_LENGTH_HCA 236
#define PDDR_STATUS_MESSAGE_LENGTH_SWITCH 59

class MlxlinkRegParser : public RegAccessParser
{
public:
    MlxlinkRegParser();
    virtual ~MlxlinkRegParser();

    void resetParser(const string& regName);
    void readMCIA(u_int32_t page, u_int32_t size, u_int32_t offset, u_int8_t* data, u_int32_t i2cAddress);
    void genBuffSendRegister(const string& regName, maccess_reg_method_t method);
    void writeGvmi(u_int32_t data);
    void updateField(string field_name, u_int32_t value);
    u_int32_t getFieldValue(string field_name);
    string getFieldStr(const string& field);
    string getRawFieldValueStr(const string fieldName);
    u_int32_t getFieldSize(string field_name);
    string getAscii(const string& name, u_int32_t size = 4);

    u_int32_t _gvmiAddress;
    MlxRegLib* _regLib;
    mfile* _mf;
    MlxlinkLogger* _mlxlinkLogger;
};

#endif /* MLXLINK_REG_PARSER_H */
