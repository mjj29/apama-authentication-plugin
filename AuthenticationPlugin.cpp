/**
 * Title:        JEMallocPlugin.cpp
 * Description:  JEMalloc EPL Plugin
 * Copyright (c) 2020 Software AG, Darmstadt, Germany and/or its licensors
 * 
 * Licensed under the Apache License, Version 2.0 (the "License"); you may not use this
 * file except in compliance with the License. You may obtain a copy of the License at
 * http:/www.apache.org/licenses/LICENSE-2.0
 * Unless required by applicable law or agreed to in writing, software distributed under the
 * License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND,
 * either express or implied.
 * See the License for the specific language governing permissions and limitations under the License.
 */

#define __STDC_FORMAT_MACROS 1
#include <epl_plugin.hpp>
#include <inttypes.h>
#include <base64.h>
#include <crypt.h>
#include <fstream>

using namespace com::apama::epl;

namespace com {
namespace apamax {

static const char alphanum[] =
	"0123456789"
	"ABCDEFGHIJKLMNOPQRSTUVWXYZ"
	"abcdefghijklmnopqrstuvwxyz";

/**
 * This plugin allows invoking the jemalloc API to force collections
 */
class AuthenticationPlugin: public EPLPlugin<AuthenticationPlugin>
{
public:
	AuthenticationPlugin() : base_plugin_t("AuthenticationPlugin")
	{
	}

	/** Export all the methods to EPL. */
	static void initialize(base_plugin_t::method_data_t &md)
	{
		md.registerMethod<decltype(&AuthenticationPlugin::base64encode), &AuthenticationPlugin::base64encode>("base64encode");
		md.registerMethod<decltype(&AuthenticationPlugin::base64decode), &AuthenticationPlugin::base64decode>("base64decode");
		md.registerMethod<decltype(&AuthenticationPlugin::hash), &AuthenticationPlugin::hash>("hash");
		md.registerMethod<decltype(&AuthenticationPlugin::generateToken), &AuthenticationPlugin::generateToken>("generateToken");
	}

	std::string base64encode(const char *input)
	{
		size_t inlen = strlen(input);
		size_t outlen = Base64::EncodedLength(inlen);
		std::unique_ptr<char[]> buf(new char[outlen+1]);
		if (!Base64::Encode(input, inlen, buf.get(), outlen)) throw std::runtime_error("Encoding Base64 string failed");
		buf[outlen] = '\0';
		return buf.get();
	}

	std::string base64decode(const char *input)
	{
		size_t inlen = strlen(input);
		size_t outlen = Base64::DecodedLength(input, inlen);
		std::unique_ptr<char[]> buf(new char[outlen+1]);
		if (!Base64::Decode(input, inlen, buf.get(), outlen)) throw std::runtime_error("Decoding Base64 string failed");
		buf[outlen] = '\0';
		return buf.get();
	}

	std::string hash(const char *input, const char *salt)
	{
		struct crypt_data data;
		data.initialized = 0;
		const char * result;
		if (std::string("") == salt) {
			char setting[11] = "$1$";
			srand(time(0));
			for (int i = 3; i < 11; ++i) {
				setting[i] = alphanum[rand()%62];
			}
			setting[10]='\0';
			result = crypt_r(input, setting, &data);
		} else {
			result = crypt_r(input, salt, &data);
		}
		return result;
	}

	std::string generateToken()
	{
		char token[65];
		char buf[64];
		std::ifstream urandom("/dev/urandom");
		urandom.read(buf, 64);
		for (int i = 0; i < 64; ++i) {
			token[i] = alphanum[buf[i]%62];
		}
		token[64]='\0';
		return token; 
	}

};

/// Export this plugin
APAMA_DECLARE_EPL_PLUGIN(AuthenticationPlugin)

}}
